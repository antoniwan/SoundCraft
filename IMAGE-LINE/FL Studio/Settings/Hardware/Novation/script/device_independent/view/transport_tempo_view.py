from math import ceil, floor

from script.actions import TempoChangedAction
from script.device_independent.util_view.view import View


class TransportTempoView(View):
    def __init__(self, action_dispatcher, fl, *, control_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.control_index = control_index

    def handle_ControlChangedAction(self, action):
        if action.control is not self.control_index:
            return
        self._increment_tempo(action.value)
        self.action_dispatcher.dispatch(TempoChangedAction())

    def _increment_tempo(self, value):
        current_tempo = self.fl.get_tempo()
        encoder_sensitivity_multiplier = 25
        value *= encoder_sensitivity_multiplier
        value = ceil(value) if value > 0 else floor(value)
        new_tempo = current_tempo + value
        self.fl.set_tempo(new_tempo)
