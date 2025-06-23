from script.constants import FaderMuteSelectMode
from script.device_independent.util_view.view import View


class MixerMuteSelectScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_MuteSelectStateChangedAction(self, action):
        text = "Select" if action.mode == FaderMuteSelectMode.Select else "Mute"
        self.screen_writer.display_notification(primary_text="Button Mode", secondary_text=text)
