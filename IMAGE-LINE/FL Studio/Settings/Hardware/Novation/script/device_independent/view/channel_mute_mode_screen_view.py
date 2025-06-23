from script.device_independent.util_view.view import View


class ChannelMuteModeScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def handle_ChannelMuteModeAction(self, action):
        # Clear the screen cache first to ensure this text is displayed
        self.screen_writer.reset()
        self.screen_writer.display_notification(primary_text="Button Mode", secondary_text="Mute")
