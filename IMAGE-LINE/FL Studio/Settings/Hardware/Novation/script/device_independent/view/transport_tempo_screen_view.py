from script.constants import DisplayPriority
from script.device_independent.util_view.view import View


class TransportTempoScreenView(View):
    def __init__(self, action_dispatcher, fl, screen_writer, *, control_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.screen_writer = screen_writer
        self.control_index = control_index

    def handle_TempoChangedAction(self, action):
        value = self.fl.get_tempo_as_string()
        self.screen_writer.display_parameter(
            self.control_index,
            title=None,
            name="Tempo",
            value=value,
            priority=DisplayPriority.Name,
        )
