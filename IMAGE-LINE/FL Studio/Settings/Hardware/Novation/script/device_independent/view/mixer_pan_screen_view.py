from script.device_independent.util_view.view import View


class MixerPanScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl

    def handle_MixerTrackPanChangedAction(self, action):
        self.display_pan(action.control, action.track, action.value)

    def handle_MixerTrackPanPreviewedAction(self, action):
        if action.track is None:
            self.screen_writer.display_parameter(action.control, title="", name="Not Used", value="")
        else:
            self.display_pan(action.control, action.track, action.value)

    def display_pan(self, control, track, value):
        pan = value
        if abs(pan) < 1e-6:
            pan_str = "C"
        elif pan < 0:
            pan_str = f'{format(abs(pan) * 100, ".0f")}L'
        else:
            pan_str = f'{format(abs(pan) * 100, ".0f")}R'

        track_name = self.fl.get_mixer_track_name(track)
        self.screen_writer.display_parameter(control, title=track_name, name="Pan", value=pan_str)
