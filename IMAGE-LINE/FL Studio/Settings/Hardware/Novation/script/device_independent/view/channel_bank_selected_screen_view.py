from script.constants import ChannelNavigationSteps
from script.device_independent.util_view.view import View


class ChannelBankSelectedScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl, model):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl
        self.model = model

    def handle_ChannelBankChangedAction(self, action):
        channel_count = self.fl.channel_count()
        channel_offset_for_bank = self.model.channel_rack.active_bank * ChannelNavigationSteps.Bank.value
        first_channel = channel_offset_for_bank + 1
        last_channel = max(0, min(channel_offset_for_bank + ChannelNavigationSteps.Bank.value, channel_count))
        self.screen_writer.display_notification(
            primary_text="Channel Rack", secondary_text=f"{first_channel}-{last_channel}"
        )
