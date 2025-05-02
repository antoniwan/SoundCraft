from script.actions import PluginParameterValueChangedAction
from script.constants import ControlChangeType, PluginParameterType
from script.device_independent.util_view.view import View
from script.device_independent.view.control_change_rate_limiter import ControlChangeRateLimiter
from script.fl_constants import PluginType, RefreshFlags
from util.deadzone import Deadzone


class PluginParameterView(View):
    channel_selection_flags = RefreshFlags.ChannelSelection.value | RefreshFlags.ChannelGroup.value
    mixer_track_selection_flags = RefreshFlags.MixerSelection.value

    def __init__(self, action_dispatcher, fl, plugin_parameters, *, control_to_index):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.plugin_parameters = plugin_parameters
        self.control_to_index = control_to_index
        self.parameters_for_index = []
        self.deadzone_for_index = []
        self.action_dispatcher = action_dispatcher
        self.reset_pickup_on_first_movement = False
        self.control_change_rate_limiter = ControlChangeRateLimiter(action_dispatcher)
        self.parameter_context_for_index = []

    def _on_show(self):
        self.control_change_rate_limiter.start()
        self._update_plugin_parameters()
        self.reset_pickup_on_first_movement = True

    def _on_hide(self):
        self.control_change_rate_limiter.stop()

    def handle_ChannelSelectAction(self, action):
        self._update_plugin_parameters()
        self.reset_pickup_on_first_movement = True

    def handle_PresetChangedAction(self, action):
        self.reset_pickup_on_first_movement = True

    def handle_OnRefreshAction(self, action):
        if not action.flags & (self.channel_selection_flags | self.mixer_track_selection_flags):
            return

        selected_plugin_type = self.fl.get_selected_plugin_type()
        if selected_plugin_type is None:
            self._update_plugin_parameters()
        if selected_plugin_type == PluginType.Instrument and action.flags & self.channel_selection_flags:
            self._update_plugin_parameters()
        if selected_plugin_type == PluginType.Effect and action.flags & self.mixer_track_selection_flags:
            self._update_plugin_parameters()

    def _update_plugin_parameters(self):
        self.control_change_rate_limiter.reset()
        plugin = self.fl.get_selected_plugin()
        if plugin in self.plugin_parameters:
            parameters = self.plugin_parameters[plugin]
            new_parameters_for_index = parameters[: len(self.control_to_index)]
            if self.parameters_for_index == new_parameters_for_index:
                return
            self.parameters_for_index = new_parameters_for_index
            self.deadzone_for_index = [None] * len(self.parameters_for_index)
            self.parameter_context_for_index = [0] * len(self.parameters_for_index)
            for index, parameter in enumerate(self.parameters_for_index):
                if parameter:
                    self.deadzone_for_index[index] = Deadzone(
                        centre=parameter.deadzone_centre, width=parameter.deadzone_width
                    )
        else:
            self.parameters_for_index = []
            self.deadzone_for_index = []

    def handle_ControlChangedAction(self, action):
        index = self.control_to_index.get(action.control)
        if index is None or index >= len(self.parameters_for_index):
            return

        parameter = self.parameters_for_index[index]
        if parameter is None:
            return

        is_absolute_control = action.control_change_type == ControlChangeType.Absolute.value
        if is_absolute_control and self.reset_pickup_on_first_movement:
            self.reset_pickup_on_first_movement = False
            self._reset_pickup()

        if parameter.parameter_type == PluginParameterType.Channel:
            current_parameter_value = self.fl.channel.get_parameter_value_normalised(parameter.index)
        else:
            current_parameter_value = self.fl.get_parameter_value(parameter.index)

        deadzone = self.deadzone_for_index[index]
        new_parameter_value = deadzone(action.control_change_type, action.value, current_parameter_value)

        self._update_value_for_plugin_parameter(
            parameter, action.control, new_parameter_value, index, is_absolute_control
        )

    def _update_value_for_plugin_parameter(self, parameter, control, position, index, is_absolute_control):
        if self.control_change_rate_limiter.forward_control_change_event(parameter.index, position):
            if parameter.parameter_type == PluginParameterType.Channel:
                if is_absolute_control:
                    self.fl.channel.set_parameter_value_normalised(parameter.index, position)
                else:
                    context = self.parameter_context_for_index[index]
                    new_context = self.fl.channel.set_parameter_value_normalised_with_context(
                        parameter.index, position, context
                    )
                    self.parameter_context_for_index[index] = new_context
            elif parameter.parameter_type == PluginParameterType.Plugin:
                if is_absolute_control:
                    self.fl.plugin.set_parameter_value(parameter.index, position)
                else:
                    context = self.parameter_context_for_index[index]
                    new_context = self.fl.plugin.set_parameter_value(parameter.index, position, context=context)
                    self.parameter_context_for_index[index] = new_context

            self.action_dispatcher.dispatch(
                PluginParameterValueChangedAction(parameter=parameter, control=control, value=position)
            )

    def _reset_pickup(self):
        for parameter in self.parameters_for_index:
            if parameter is not None and parameter.parameter_type is PluginParameterType.Plugin:
                self.fl.reset_parameter_pickup(parameter.index)
