from script.actions import MixerTrackEqPreviewedAction
from script.constants import Encoders, EqBand, EqParameter
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class MixerTrackEqPreviewView(View):
    controls = [
        (EqParameter.Frequency, EqBand.LowShelf.value),
        (EqParameter.Gain, EqBand.LowShelf.value),
        (EqParameter.Frequency, EqBand.Peaking.value),
        (EqParameter.Gain, EqBand.Peaking.value),
        (EqParameter.Frequency, EqBand.HighShelf.value),
        (EqParameter.Gain, EqBand.HighShelf.value),
    ]

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.MixerControls.value:
            self._update_previews()

    def handle_MixerBankChangedAction(self, action):
        self._update_previews()

    def _update_previews(self):
        for index, control in enumerate(self.controls):
            eq_parameter, band = control
            self.action_dispatcher.dispatch(
                MixerTrackEqPreviewedAction(control=index, band=band, parameter=eq_parameter)
            )

        for control in range(len(self.controls), Encoders.Num.value):
            self.action_dispatcher.dispatch(MixerTrackEqPreviewedAction(band=None, parameter=None, control=control))
