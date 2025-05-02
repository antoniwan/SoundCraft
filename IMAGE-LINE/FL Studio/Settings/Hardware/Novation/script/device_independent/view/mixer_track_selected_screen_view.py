from script.device_independent.util_view.view import View
from script.fl_constants import FlConstants


class MixerTrackSelectedScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl, *, show_index_in_primary_text=False):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl
        self.show_index_in_primary_text = show_index_in_primary_text

    def handle_MixerTrackSelectedAction(self, action):
        index = self.fl.get_selected_mixer_track()
        name = self.fl.get_mixer_track_name(index)
        if self.show_index_in_primary_text:
            primary_text = "Track" if index == FlConstants.MasterTrackIndex else f"Track {index}"
            secondary_text = name
        else:
            primary_text = "Track"
            secondary_text = name if index == FlConstants.MasterTrackIndex else f"{index} - {name}"
        self.screen_writer.display_notification(primary_text=primary_text, secondary_text=secondary_text)
