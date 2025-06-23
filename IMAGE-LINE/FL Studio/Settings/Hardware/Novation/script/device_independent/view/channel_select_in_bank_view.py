from script.actions import ChannelSelectAction
from script.colour_utils import clamp_brightness, scale_colour
from script.colours import Colours
from script.constants import ChannelNavigationSteps, LedLightingType
from script.device_independent.util_view import View
from script.fl_constants import RefreshFlags


class ChannelSelectInBankView(View):
    button_functions = [
        "ChannelSelect_1",
        "ChannelSelect_2",
        "ChannelSelect_3",
        "ChannelSelect_4",
        "ChannelSelect_5",
        "ChannelSelect_6",
        "ChannelSelect_7",
        "ChannelSelect_8",
    ]
    select_function = "ChannelSelect"

    def __init__(self, action_dispatcher, product_defs, fl, model, button_led_writer):
        super().__init__(action_dispatcher)
        self.action_dispatcher = action_dispatcher
        self.product_defs = product_defs
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.model = model
        self.bright_colour_min_brightness = 100
        self.dim_colour_scale_factor = 0.25

    def _on_show(self):
        self.update_leds()

    def _on_hide(self):
        self.turn_off_leds()

    @property
    def channels_in_bank(self):
        channel_offset_for_bank = self.model.channel_rack.active_bank * ChannelNavigationSteps.Bank.value
        return [
            channel_offset_for_bank + channel
            for channel in range(ChannelNavigationSteps.Bank.value)
            if channel_offset_for_bank + channel < self.fl.channel_count()
        ]

    @property
    def button_to_channel_index(self):
        channels_in_bank = self.channels_in_bank
        return {
            self.product_defs.FunctionToButton.get(function): channel
            for function, channel in zip(self.button_functions, channels_in_bank)
        }

    def handle_ButtonPressedAction(self, action):
        if action.button in self.button_to_channel_index:
            channel_index = self.button_to_channel_index[action.button]
            self._select_channel(channel_index)

    def handle_ChannelBankChangedAction(self, action):
        self.update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.LedUpdate.value:
            self.update_leds()

    def get_colour_for_channel(self, channel_index):
        channel_colour = self.fl.get_channel_colour(group_channel=channel_index)
        if self._is_channel_selected(channel_index):
            return self.bright_channel_colour(channel_colour)
        return self.dim_channel_colour(channel_colour)

    def update_leds(self):
        self.turn_off_leds()
        select_button = self.product_defs.FunctionToButton.get(self.select_function)
        self.button_led_writer.set_button_colour(select_button, Colours.channel_select)
        for button, channel_index in self.button_to_channel_index.items():
            colour = self.get_colour_for_channel(channel_index)
            self.button_led_writer.set_button_colour(button, colour, lighting_type=LedLightingType.RGB)

    def turn_off_leds(self):
        select_button = self.product_defs.FunctionToButton.get(self.select_function)
        self.button_led_writer.set_button_colour(select_button, Colours.off)
        for function in self.button_functions:
            button = self.product_defs.FunctionToButton.get(function)
            self.button_led_writer.set_button_colour(button, Colours.off)

    def dim_channel_colour(self, base_colour):
        return scale_colour(base_colour, self.dim_colour_scale_factor)

    def bright_channel_colour(self, base_colour):
        return clamp_brightness(base_colour, minimum=self.bright_colour_min_brightness)

    def _select_channel(self, channel_index):
        if not self._is_channel_selected(channel_index):
            self.fl.select_channel_exclusively(channel_index)
            self.action_dispatcher.dispatch(ChannelSelectAction())

    def _is_channel_selected(self, channel_index):
        return channel_index == self.fl.selected_channel() and self.fl.is_any_channel_selected()
