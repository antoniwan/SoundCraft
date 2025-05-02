from script.constants import FaderArmMuteMode
from script.device_independent.util_view.view import View


class MixerArmMuteScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_ArmSelectStateChangedAction(self, action):
        text = "Mute" if action.mode == FaderArmMuteMode.Mute else "Arm"
        self.screen_writer.display_notification(primary_text="Button Mode", secondary_text=text)
