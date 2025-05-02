from script.actions import ChannelVolumePreviewedAction
from script.constants import Pots
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class ChannelRackVolumePreviewView(View):
    channels_per_bank = Pots.Num.value

    def __init__(self, action_dispatcher, product_defs, model):
        super().__init__(action_dispatcher)
        self.product_defs = product_defs
        self.model = model

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.PluginValue.value:
            self._update_previews()

    def handle_ChannelBankChangedAction(self, action):
        self._update_previews()

    def _update_previews(self):
        start_channel = self.model.channel_rack.active_bank * self.channels_per_bank
        for control, channel in enumerate(range(start_channel, start_channel + self.channels_per_bank)):
            self.action_dispatcher.dispatch(ChannelVolumePreviewedAction(channel=channel, control=control))
