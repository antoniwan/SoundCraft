from script.device_independent.util_view.view import View


class LedView(View):
    def __init__(self, action_dispatcher, product_defs, led_writer, *, cc, colour):
        super().__init__(action_dispatcher)
        self.product_defs = product_defs
        self.led_writer = led_writer
        self.cc = cc
        self.colour = colour

    def _on_show(self):
        self._update_led(self.colour)

    def _update_led(self, colour):
        self.led_writer.set_pad_colour(self.cc, colour, target=self.product_defs.Constants.LightingTargetCC.value)
