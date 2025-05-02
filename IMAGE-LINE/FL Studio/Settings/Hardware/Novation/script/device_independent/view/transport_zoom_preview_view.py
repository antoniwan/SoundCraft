from script.constants import DisplayPriority
from script.device_independent.util_view.view import View


class TransportZoomPreviewView(View):
    def __init__(self, action_dispatcher, product_defs, screen_writer, *, control_index):
        super().__init__(action_dispatcher)
        self.product_defs = product_defs
        self.screen_writer = screen_writer
        self.control_index = control_index

    def _on_show(self):
        self._update_preview()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("PreviewModifier"):
            self._update_preview()

    def _update_preview(self):
        self.screen_writer.display_parameter(
            self.control_index,
            title="",
            name="Zoom",
            value="",
            priority=DisplayPriority.Name,
        )
