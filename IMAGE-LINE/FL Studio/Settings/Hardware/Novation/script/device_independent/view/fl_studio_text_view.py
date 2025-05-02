from script.device_independent.util_view.view import View


class FLStudioTextView(View):
    def __init__(self, screen_writer, action_dispatcher):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer

    def _on_show(self):
        self.screen_writer.display_idle("FL Studio")

    def _on_hide(self):
        self.screen_writer.display_idle("")
