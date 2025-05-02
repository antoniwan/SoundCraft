from script.actions import SongPositionChangedAction
from script.device_independent.util_view.view import View


class TransportSongPositionView(View):
    def __init__(self, action_dispatcher, fl, *, control_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.control_index = control_index

    def handle_ControlChangedAction(self, action):
        if action.control is not self.control_index:
            return
        self._increment_beat(action.value)
        self.action_dispatcher.dispatch(SongPositionChangedAction())

    def _increment_beat(self, value):
        ticks_per_beat = self.fl.get_ticks_per_beat()
        current_position = self.fl.transport_get_song_position_in_ticks()
        ticks_from_beat = current_position % ticks_per_beat
        new_position = current_position - ticks_from_beat
        if ticks_from_beat == 0 or value > 0:
            new_position += (1 if value > 0 else -1) * ticks_per_beat
        self.fl.transport_set_song_position_in_ticks(new_position)
