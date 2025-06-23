from script.constants import Encoders
from script.device_independent.view import (
    FLStudioTextView,
    PluginParameterPreviewView,
    PluginParameterScreenView,
    PluginParameterView,
)
from script.plugin import plugin_parameter_mappings
from util.control_to_index import make_control_to_index


class PluginEncoderLayoutManager:
    def __init__(self, action_dispatcher, fl, product_defs, screen_writer, device_manager):
        self.device_manager = device_manager
        self.screen_writer = screen_writer
        control_to_index = make_control_to_index(Encoders.FirstControlIndex.value, Encoders.Num.value)
        self.views = [
            FLStudioTextView(screen_writer, action_dispatcher),
            PluginParameterView(action_dispatcher, fl, plugin_parameter_mappings, control_to_index=control_to_index),
            PluginParameterScreenView(
                action_dispatcher, fl, screen_writer, plugin_parameter_mappings, control_to_index=control_to_index
            ),
            PluginParameterPreviewView(
                action_dispatcher,
                fl,
                product_defs,
                plugin_parameter_mappings,
                control_to_index=control_to_index,
            ),
        ]

    def show(self):
        self.device_manager.enable_encoder_mode()

        for view in self.views:
            view.show()

    def hide(self):
        for view in self.views:
            view.hide()

    def focus_windows(self):
        pass
