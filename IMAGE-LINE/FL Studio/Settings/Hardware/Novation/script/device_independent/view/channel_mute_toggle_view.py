from script.actions import ChannelMuteStateChangedAction
from script.colour_utils import clamp_brightness, scale_colour
from script.colours import Colours
from script.constants import ChannelNavigationSteps, LedLightingType
from script.device_independent.util_view import View
from script.fl_constants import RefreshFlags


class ChannelMuteToggleView(View):
    button_functions = [
        "ToggleMute_1",
        "ToggleMute_2",
        "ToggleMute_3",
        "ToggleMute_4",
        "ToggleMute_5",
        "ToggleMute_6",
        "ToggleMute_7",
        "ToggleMute_8",
    ]
    mute_function = "Mute"

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
            self._toggle_mute(channel_index)

    def handle_ChannelBankChangedAction(self, action):
        self.update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.LedUpdate.value:
            self.update_leds()

    def get_colour_for_channel(self, channel_index):
        channel_colour = self.fl.get_channel_colour(group_channel=channel_index)
        if not self.fl.is_channel_mute_enabled(group_channel=channel_index):
            return self.bright_channel_colour(channel_colour)
        return self.dim_channel_colour(channel_colour)

    def update_leds(self):
        self.turn_off_leds()
        mute_button = self.product_defs.FunctionToButton.get(self.mute_function)
        self.button_led_writer.set_button_colour(mute_button, Colours.button_toggle_on)
        for button, channel_index in self.button_to_channel_index.items():
            colour = self.get_colour_for_channel(channel_index)
            self.button_led_writer.set_button_colour(button, colour, lighting_type=LedLightingType.RGB)

    def turn_off_leds(self):
        mute_button = self.product_defs.FunctionToButton.get(self.mute_function)
        self.button_led_writer.set_button_colour(mute_button, Colours.off)
        for function in self.button_functions:
            button = self.product_defs.FunctionToButton.get(function)
            self.button_led_writer.set_button_colour(button, Colours.off)

    def dim_channel_colour(self, base_colour):
        return scale_colour(base_colour, self.dim_colour_scale_factor)

    def bright_channel_colour(self, base_colour):
        return clamp_brightness(base_colour, minimum=self.bright_colour_min_brightness)

    def _toggle_mute(self, channel_index):
        enabled = not self.fl.is_channel_mute_enabled(group_channel=channel_index)
        self.fl.toggle_channel_mute(group_channel=channel_index)
        self.action_dispatcher.dispatch(ChannelMuteStateChangedAction(channel=channel_index, enabled=enabled))
