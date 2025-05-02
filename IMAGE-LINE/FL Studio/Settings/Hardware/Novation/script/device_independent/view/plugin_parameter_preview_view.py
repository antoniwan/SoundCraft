from script.actions import PluginParameterValuePreviewedAction
from script.constants import Encoders, PluginParameterType
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class PluginParameterPreviewView(View):
    def __init__(self, action_dispatcher, fl, product_defs, plugin_parameters, *, control_to_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.product_defs = product_defs
        self.plugin_parameters = plugin_parameters
        self.control_to_index = control_to_index
        self.parameters_for_index = []

    def _on_show(self):
        self._update_previews()

    def handle_OnRefreshAction(self, action):
        if action.flags & (RefreshFlags.PluginValue.value | RefreshFlags.ChannelSelection.value):
            self._update_previews()

    def _update_previews(self):
        self._update_plugin_parameters()
        for index in range(Encoders.Num.value):
            self._update_preview(index)

    def _update_preview(self, index):
        parameter = self.parameters_for_index[index] if index < len(self.parameters_for_index) else None
        value = None
        if parameter:
            if parameter.parameter_type == PluginParameterType.Channel:
                value = self.fl.channel.get_parameter_value_normalised(parameter.index)
            else:
                value = self.fl.get_parameter_value(parameter.index)
        self.action_dispatcher.dispatch(
            PluginParameterValuePreviewedAction(parameter=parameter, control=index, value=value)
        )

    def _update_plugin_parameters(self):
        plugin = self.fl.get_selected_plugin()
        if plugin in self.plugin_parameters:
            parameters = self.plugin_parameters[plugin]
            self.parameters_for_index = parameters[: len(self.control_to_index)]
        else:
            self.parameters_for_index = []
