from script.actions import MixerTrackVolumePreviewedAction
from script.constants import Encoders
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class MixerVolumePreviewView(View):
    def __init__(self, action_dispatcher, product_defs, model):
        super().__init__(action_dispatcher)
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
            self.action_dispatcher.dispatch(MixerTrackVolumePreviewedAction(track=track, control=index))
        for control in range(index + 1, Encoders.Num.value):
            self.action_dispatcher.dispatch(MixerTrackVolumePreviewedAction(track=None, control=control))
