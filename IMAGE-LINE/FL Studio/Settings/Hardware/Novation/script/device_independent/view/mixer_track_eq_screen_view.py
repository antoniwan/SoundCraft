from script.constants import EqParameter
from script.device_independent.util_view.view import View


class MixerTrackEqScreenView(View):
    band_names = ["Low Shelf", "Peaking", "High Shelf"]

    def __init__(self, action_dispatcher, screen_writer, fl):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl

    def handle_MixerTrackEqChangedAction(self, action):
        self.display_eq(action.control, action.band, action.parameter)

    def handle_MixerTrackEqPreviewedAction(self, action):
        if action.band is None:
            self.screen_writer.display_parameter(action.control, title="", name="Not Used", value="")
        else:
            self.display_eq(action.control, action.band, action.parameter)

    def display_eq(self, control, band, parameter):
        band_name = self.band_names[band]
        track_name = self.fl.get_mixer_track_name(self.fl.get_selected_mixer_track())
        if parameter == EqParameter.Gain.value:
            value = self.fl.get_mixer_track_eq_gain_as_string(band)
        else:
            value = self.fl.get_mixer_track_eq_frequency_as_string(band)
        self.screen_writer.display_parameter(control, title=track_name, name=band_name, value=value)
