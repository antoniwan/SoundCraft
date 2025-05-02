from script.actions import MixerTrackPanPreviewedAction
from script.constants import Encoders
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class MixerPanPreviewView(View):
    def __init__(self, action_dispatcher, fl, product_defs, model):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.product_defs = product_defs
        self.model = model

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.MixerControls.value:
            self._update_previews()

    def handle_MixerBankChangedAction(self, action):
        self._update_previews()

    def _update_previews(self):
        for index, track in enumerate(self.model.mixer_tracks_in_active_bank):
            pan_position = self.fl.get_mixer_track_pan(track)
            self.action_dispatcher.dispatch(
                MixerTrackPanPreviewedAction(track=track, control=index, value=pan_position)
            )
        for control in range(index + 1, Encoders.Num.value):
            self.action_dispatcher.dispatch(MixerTrackPanPreviewedAction(track=None, control=control, value=None))
