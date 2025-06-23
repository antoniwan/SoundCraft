from script.actions import MixerTrackEqChangedAction
from script.colours import Colours
from script.constants import EqBand, EqParameter, Pots
from script.device_independent.util_view import View
from script.fl_constants import RefreshFlags
from util.deadzone import RelativeDeadzone


class MixerTrackEqView(View):
    controls = [
        (EqParameter.Frequency, EqBand.LowShelf.value),
        (EqParameter.Gain, EqBand.LowShelf.value),
        (EqParameter.Frequency, EqBand.Peaking.value),
        (EqParameter.Gain, EqBand.Peaking.value),
        (EqParameter.Frequency, EqBand.HighShelf.value),
        (EqParameter.Gain, EqBand.HighShelf.value),
    ]

    def __init__(self, action_dispatcher, fl, product_defs=None, led_writer=None, *, control_to_index):
        super().__init__(action_dispatcher)
        self.action_dispatcher = action_dispatcher
        self.fl = fl
        self.control_to_index = control_to_index
        self.deadzone_for_index = []
        self.product_defs = product_defs
        self.led_writer = led_writer

    def _on_show(self):
        self._update_parameters()
        self._update_leds()

    def handle_ControlChangedAction(self, action):
        index = self.control_to_index.get(action.control)
        if index is None or index >= len(self.controls):
            return

        eq_parameter, band = self.controls[index]
        deadzone = self.deadzone_for_index[index]
        if eq_parameter == EqParameter.Gain:
            value = deadzone(action.value, self.fl.get_mixer_track_eq_gain(band))
            self.fl.set_mixer_track_eq_gain(band, value)
        else:
            value = deadzone(action.value, self.fl.get_mixer_track_eq_frequency(band))
            self.fl.set_mixer_track_eq_frequency(band, value)

        self.action_dispatcher.dispatch(
            MixerTrackEqChangedAction(control=action.control, band=band, parameter=eq_parameter)
        )

    def handle_MixerTrackSelectedAction(self, action):
        self._update_parameters()
        self._update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.MixerSelection.value:
            self._update_parameters()

    def _update_parameters(self):
        control_num = len(self.controls)
        self.deadzone_for_index = [None] * control_num

        for index, control in enumerate(self.controls):
            eq_parameter, band = control
            if eq_parameter == EqParameter.Gain:
                self.deadzone_for_index[index] = RelativeDeadzone(maximum=1.0, centre=0.5, width=0.05)
            else:
                self.deadzone_for_index[index] = RelativeDeadzone(maximum=1.0, centre=None, width=0.05)

    def _update_leds(self):
        if self.led_writer is None or self.product_defs is None:
            return

        encoder_first_index = self.product_defs.Constants.EqControlFirstIndex.value
        encoder_cc_offset = encoder_first_index + self.product_defs.Constants.EncoderCcOffset.value
        for index, control in enumerate(self.controls):
            encoder = self.control_to_index.get(index + encoder_first_index) + encoder_cc_offset
            eq_parameter, band = control
            colour = Colours.eq_parameter_gain if eq_parameter == EqParameter.Gain else Colours.eq_parameter_frequency
            self.led_writer.set_pad_colour(encoder, colour, target=self.product_defs.Constants.LightingTargetCC.value)
        for index in range(len(self.controls), Pots.Num.value):
            encoder = self.control_to_index.get(index + encoder_first_index) + encoder_cc_offset
            self.led_writer.set_pad_colour(
                encoder, Colours.off, target=self.product_defs.Constants.LightingTargetCC.value
            )
