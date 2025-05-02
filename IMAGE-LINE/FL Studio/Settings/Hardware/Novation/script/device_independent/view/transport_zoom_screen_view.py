from script.constants import DisplayPriority, Zoom
from script.device_independent.util_view.view import View


class TransportZoomScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, *, control_index):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.control_index = control_index

    def handle_HorZoomChangedAction(self, action):
        self.screen_writer.display_parameter(
            self.control_index,
            title=None,
            name="Zoom",
            value="In" if action.value == Zoom.In.value else "Out",
            priority=DisplayPriority.Name,
        )
