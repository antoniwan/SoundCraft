from script.device_independent.view import FLStudioTextView


class GenericEncoderLayoutManager:
    def __init__(self, action_dispatcher, screen_writer):
        self.views = [
            FLStudioTextView(screen_writer, action_dispatcher),
        ]

    def show(self):
        for view in self.views:
            view.show()

    def hide(self):
        for view in self.views:
            view.hide()

    def focus_windows(self):
        pass
