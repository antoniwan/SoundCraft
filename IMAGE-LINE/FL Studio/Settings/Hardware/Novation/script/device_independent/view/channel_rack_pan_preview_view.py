from script.actions import ChannelPanPreviewedAction
from script.constants import Pots
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class ChannelRackPanPreviewView(View):
    channels_per_bank = Pots.Num.value

    def __init__(self, action_dispatcher, fl, product_defs, model):
        super().__init__(action_dispatcher)
        self.fl = fl
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
        channel_count = self.fl.channel_count()
        start_channel = self.model.channel_rack.active_bank * self.channels_per_bank
        for control, channel in enumerate(range(start_channel, start_channel + self.channels_per_bank)):
            value = self.fl.get_channel_pan(channel) if channel < channel_count else 0
            self.action_dispatcher.dispatch(ChannelPanPreviewedAction(channel=channel, control=control, value=value))
