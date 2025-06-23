from script.colours import Colours
from script.constants import Encoders
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class PluginParameterLedView(View):
    def __init__(self, action_dispatcher, led_writer, fl, product_defs, plugin_parameters, *, control_to_index):
        super().__init__(action_dispatcher)
        self.led_writer = led_writer
        self.fl = fl
        self.product_defs = product_defs
        self.plugin_parameters = plugin_parameters
        self.control_to_index = control_to_index
        self.parameters_for_index = []

    def _on_show(self):
        self._update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & (RefreshFlags.PluginValue.value | RefreshFlags.ChannelSelection.value):
            self._update_leds()

    def _update_leds(self):
        self._update_plugin_parameters()
        for index in range(Encoders.Num.value):
            self._update_led(index)

    def _update_led(self, index):
        parameter = self.parameters_for_index[index] if index < len(self.parameters_for_index) else None
        colour = Colours.plugin_parameter if parameter else Colours.off
        encoder_first_index = self.product_defs.Constants.PluginParameterFirstIndex.value
        encoder_cc_offset = encoder_first_index + self.product_defs.Constants.EncoderCcOffset.value
        encoder = self.control_to_index.get(index + encoder_first_index) + encoder_cc_offset
        self.led_writer.set_pad_colour(encoder, colour, target=self.product_defs.Constants.LightingTargetCC.value)

    def _update_plugin_parameters(self):
        plugin = self.fl.get_selected_plugin()
        if plugin in self.plugin_parameters:
            parameters = self.plugin_parameters[plugin]
            self.parameters_for_index = parameters[: len(self.control_to_index)]
        else:
            self.parameters_for_index = []
