from script.device_independent.util_view.view import View


class TransportIdleScreenView(View):
    def __init__(self, action_dispatcher, screen_writer):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def _on_show(self):
        self.screen_writer.display_idle("Transport", ("Scrb", "Zoom", None, None, "Mark", None, None, "BPM"))

    def _on_hide(self):
        self.screen_writer.display_idle("")
