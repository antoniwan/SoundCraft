from script.actions import HorZoomChangedAction
from script.constants import Zoom
from script.device_independent.util_view.view import View


class TransportZoomView(View):
    def __init__(self, action_dispatcher, fl, *, control_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.control_index = control_index

    def handle_ControlChangedAction(self, action):
        if action.control == self.control_index:
            value = (Zoom.In if action.value > 0 else Zoom.Out).value
            self.fl.ui.horizontal_zoom(value)
            self.action_dispatcher.dispatch(HorZoomChangedAction(value=value))
