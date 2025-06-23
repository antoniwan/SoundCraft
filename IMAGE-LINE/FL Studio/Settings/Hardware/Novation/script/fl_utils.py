class FlUtils:
    def __init__(self, fl):
        self.fl = fl

    def get_mixer_tracks_for_dock_side(self, dock_side):
        return [
            track
            for track in range(self.fl.mixer_track_count() + 1)
            if self.fl.get_dock_side_for_track(track) is dock_side
            and track != self.fl.get_mixer_current_track_special_index()
        ]
