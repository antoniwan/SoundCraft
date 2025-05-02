from script.actions import MarkerSelectBlockedAction, NextMarkerSelectedAction, PreviousMarkerSelectedAction
from script.device_independent.util_view.view import View
from script.fl_constants import LoopMode


class TransportMarkerView(View):
    def __init__(self, action_dispatcher, fl, *, control_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.control_index = control_index
        self.damperValue = 0
        self.damperThreshold = 3

    def handle_ControlChangedAction(self, action):
        if action.control != self.control_index:
            return

        if self.fl.transport_get_loop_mode() == LoopMode.Pattern:
            self.action_dispatcher.dispatch(MarkerSelectBlockedAction(message="Pattern mode"))
            return

        self.fl.ui.focus_playlist_window()
        if action.control == self.control_index:
            self.damperValue += 1 if action.value > 0 else -1
            if self.damperValue > self.damperThreshold:
                self.damperValue = 0
                self.fl.transport_go_to_next_marker()
                self.action_dispatcher.dispatch(NextMarkerSelectedAction())
            elif self.damperValue < -self.damperThreshold:
                self.damperValue = 0
                self.fl.transport_go_to_previous_marker()
                self.action_dispatcher.dispatch(PreviousMarkerSelectedAction())
