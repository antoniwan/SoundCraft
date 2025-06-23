from script.constants import Pots
from script.device_independent.view import (
    ChannelBankControlsHighlightView,
    ChannelRackVolumeScreenView,
    ChannelRackVolumeView,
)
from util.control_to_index import make_control_to_index


class ChannelVolumePotLayoutManager:
    def __init__(self, action_dispatcher, fl, screen_writer, model, fl_window_manager):
        self.fl_window_manager = fl_window_manager
        control_to_index = make_control_to_index(Pots.FirstControlIndex.value, Pots.Num.value)
        self.views = {
            ChannelBankControlsHighlightView(action_dispatcher, fl, model),
            ChannelRackVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index),
            ChannelRackVolumeScreenView(action_dispatcher, screen_writer, fl),
        }

    def show(self):
        for view in self.views:
            view.show()

    def hide(self):
        for view in self.views:
            view.hide()

    def focus_windows(self):
        self.fl_window_manager.hide_last_focused_plugin_window()
        self.fl_window_manager.focus_channel_window()
