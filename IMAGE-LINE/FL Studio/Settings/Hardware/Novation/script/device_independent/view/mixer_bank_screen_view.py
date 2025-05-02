from script.device_independent.util_view.view import View


class MixerBankScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, model):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.model = model
        self.track_cache = {}

    def handle_MixerBankChangedAction(self, action):
        tracks = self.model.mixer_tracks_in_active_bank
        first, last = tracks[0], tracks[-1]
        args = (first, last)
        if args != self.track_cache:
            self.track_cache = args
            self.screen_writer.display_notification(primary_text="Mixer Tracks", secondary_text=f"{first}-{last}")
