from script.constants import DisplayPriority
from script.device_independent.util_view.view import View


class TransportMarkerScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, *, control_index):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.control_index = control_index
        self.control_name = "Marker"

    def handle_MarkerSelectBlockedAction(self, action):
        self.screen_writer.display_parameter(
            self.control_index,
            title=None,
            name=self.control_name,
            value=action.message,
            priority=DisplayPriority.Name,
        )

    def handle_NextMarkerSelectedAction(self, action):
        self._update_screen("Next")

    def handle_PreviousMarkerSelectedAction(self, action):
        self._update_screen("Previous")

    def _update_screen(self, value):
        self.screen_writer.display_parameter(
            self.control_index,
            title=None,
            name=self.control_name,
            value=value,
            priority=DisplayPriority.Name,
        )
