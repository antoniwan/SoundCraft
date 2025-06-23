from script.constants import FaderSoloArmMode
from script.device_independent.util_view.view import View


class MixerSoloArmScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_SoloArmStateChangedAction(self, action):
        text = "Solo" if action.mode == FaderSoloArmMode.Solo else "Arm"
        self.screen_writer.display_notification(primary_text="Button Mode", secondary_text=text)
