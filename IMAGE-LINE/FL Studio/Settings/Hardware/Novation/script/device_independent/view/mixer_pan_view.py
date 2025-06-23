import util.math_helpers
from script.actions import MixerTrackPanChangedAction
from script.colours import Colours
from script.constants import ControlChangeType, Pots
from script.device_independent.util_view.view import View
from util.deadzone import Deadzone


class MixerPanView(View):
    tracks_per_bank = Pots.Num.value

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

    def handle_MixerBankChangedAction(self, action):
        self.reset_pickup_on_first_movement = True
        self._update_leds()

    def handle_ControlChangedAction(self, action):
        index = self.control_to_index.get(action.control)
        if index is None or index >= len(self.model.mixer_tracks_in_active_bank):
            return

        is_absolute_control = action.control_change_type == ControlChangeType.Absolute.value
        if is_absolute_control and self.reset_pickup_on_first_movement:
            self.reset_pickup_on_first_movement = False
            self._reset_pickup_for_current_mixer_bank()

        track = self.model.mixer_tracks_in_active_bank[index]
        current_track_pan = util.math_helpers.normalised_bipolar_to_unipolar(self.fl.get_mixer_track_pan(track))

        normalised_position = self.deadzone(action.control_change_type, action.value, current_track_pan)

        pan_position = util.math_helpers.normalised_unipolar_to_bipolar(normalised_position)
        self.fl.set_mixer_track_pan(track, pan_position)

        self.action_dispatcher.dispatch(
            MixerTrackPanChangedAction(track=track, control=action.control, value=pan_position)
        )

    def _reset_pickup_for_current_mixer_bank(self):
        for track in self.model.mixer_tracks_in_active_bank:
            self.fl.reset_track_pan_pickup(track)

    def _update_leds(self):
        if self.led_writer is None or self.product_defs is None:
            return

        encoder_first_index = self.product_defs.Constants.PanControlFirstIndex.value
        encoder_cc_offset = encoder_first_index + self.product_defs.Constants.EncoderCcOffset.value
        for index in range(self.tracks_per_bank):
            encoder = self.control_to_index.get(index + encoder_first_index) + encoder_cc_offset
            colour = Colours.mixer_track_pan if index < len(self.model.mixer_tracks_in_active_bank) else Colours.off
            self.led_writer.set_pad_colour(encoder, colour, target=self.product_defs.Constants.LightingTargetCC.value)
