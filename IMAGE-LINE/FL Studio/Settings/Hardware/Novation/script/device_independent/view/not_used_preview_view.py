from script.constants import DisplayPriority
from script.device_independent.util_view.view import View


class NotUsedPreviewView(View):
    def __init__(self, action_dispatcher, product_defs, screen_writer, *, control_index):
        super().__init__(action_dispatcher)
        self.control_index = control_index
        self.product_defs = product_defs
        self.screen_writer = screen_writer

    def _on_show(self):
        self._update_preview()

    def _update_preview(self):
        self.screen_writer.display_parameter(
            self.control_index,
            title="",
            name="Not Used",
            value="",
            priority=DisplayPriority.Name,
        )
