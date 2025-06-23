import util.math_helpers
from script.actions import ChannelPanChangedAction
from script.colours import Colours
from script.constants import ChannelNavigationMode, ChannelNavigationSteps, ControlChangeType, Pots
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags
from util.deadzone import Deadzone


class ChannelRackPanView(View):
    channels_per_bank = Pots.Num.value

    def __init__(self, action_dispatcher, fl, model, product_defs=None, led_writer=None, *, control_to_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.model = model
        self.action_dispatcher = action_dispatcher
        self.control_to_index = control_to_index
        self.deadzone = Deadzone(maximum=1.0, centre=0.5, width=0.1)
        self.reset_pickup_on_first_movement = False
        self.product_defs = product_defs
        self.led_writer = led_writer

    def _on_show(self):
        self.reset_pickup_on_first_movement = True
        self._update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.PluginValue.value:
            self._update_leds()

    def handle_ChannelBankChangedAction(self, action):
        self.reset_pickup_on_first_movement = True
        self._update_leds()

    def handle_ChannelSelectAction(self, action):
        if self.model.channel_rack.navigation_mode == ChannelNavigationMode.Single.value:
            self._reset_pickup_for_current_channel_bank()

    def handle_ControlChangedAction(self, action):
        index = self.control_to_index.get(action.control)
        if index is None:
            return

        navigation_mode = self.model.channel_rack.navigation_mode
        if navigation_mode is None:
            return

        if navigation_mode == ChannelNavigationMode.Bank.value:
            channel_offset = self.model.channel_rack.active_bank * ChannelNavigationSteps.Bank.value
        elif navigation_mode == ChannelNavigationMode.Single.value:
            channel_offset = self.fl.selected_channel()

        channel = channel_offset + index
        if channel >= self.fl.channel_count():
            return

        is_absolute_control = action.control_change_type == ControlChangeType.Absolute.value
        if is_absolute_control and self.reset_pickup_on_first_movement:
            self.reset_pickup_on_first_movement = False
            self._reset_pickup_for_current_channel_bank()

        current_channel_pan = util.math_helpers.normalised_bipolar_to_unipolar(self.fl.get_channel_pan(channel))
        normalised_position = self.deadzone(action.control_change_type, action.value, current_channel_pan)
        pan_position = util.math_helpers.normalised_unipolar_to_bipolar(normalised_position)

        self.fl.set_channel_pan(channel, pan_position)

        self.action_dispatcher.dispatch(
            ChannelPanChangedAction(channel=channel, control=action.control, value=pan_position)
        )

    def _reset_pickup_for_current_channel_bank(self):
        start_channel = self.model.channel_rack.active_bank * self.channels_per_bank
        for channel in range(start_channel, start_channel + self.channels_per_bank):
            if channel >= self.fl.channel_count():
                break
            self.fl.reset_channel_pan_pickup(channel)

    def _update_leds(self):
        if self.led_writer is None or self.product_defs is None:
            return

        encoder_first_index = self.product_defs.Constants.PanControlFirstIndex.value
        encoder_cc_offset = encoder_first_index + self.product_defs.Constants.EncoderCcOffset.value
        channel_offset = self.model.channel_rack.active_bank * ChannelNavigationSteps.Bank.value
        channel_count = self.fl.channel_count()
        for index in range(self.channels_per_bank):
            channel = channel_offset + index
            encoder = self.control_to_index.get(index + encoder_first_index) + encoder_cc_offset
            colour = Colours.channel_rack_pan if channel < channel_count else Colours.off
            self.led_writer.set_pad_colour(encoder, colour, target=self.product_defs.Constants.LightingTargetCC.value)
