from script.actions import MixerTrackPanPreviewedAction
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class MixerPanPreviewView(View):
    def __init__(self, action_dispatcher, fl, product_defs, model, *, control_to_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.product_defs = product_defs
        self.model = model
        self.control_to_index = control_to_index

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.MixerControls.value:
            self._update_previews()

    def handle_MixerBankChangedAction(self, action):
        self._update_previews()

    def _update_previews(self):
        first_track = self.model.mixer_tracks_in_active_bank[0]
        num_tracks = len(self.model.mixer_tracks_in_active_bank)
        for control, index in self.control_to_index.items():
            if index < num_tracks:
                track = first_track + index
                pan_position = self.fl.get_mixer_track_pan(track)
            else:
                track = None
                pan_position = None
            self.action_dispatcher.dispatch(
                MixerTrackPanPreviewedAction(track=track, control=control, value=pan_position)
            )
