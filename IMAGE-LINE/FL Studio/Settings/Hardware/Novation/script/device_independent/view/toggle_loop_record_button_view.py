from script.colours import Colours
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class ToggleLoopRecordButtonView(View):
    def __init__(self, action_dispatcher, button_led_writer, fl, product_defs):
        super().__init__(action_dispatcher)
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.product_defs = product_defs

    def _on_show(self):
        self.update_led()

    def _on_hide(self):
        self.turn_off_led()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ToggleLoopRecord"):
            self.fl.toggle_loop_record()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.TransportStatus.value:
            self.update_led()

    def update_led(self):
        active = self.fl.loop_record_is_active()
        self.button_led_writer.set_button_colour(
            self.product_defs.FunctionToButton.get("ToggleLoopRecord"),
            Colours.button_toggle_on if active else Colours.off,
        )

    def turn_off_led(self):
        self.button_led_writer.set_button_colour(
            self.product_defs.FunctionToButton.get("ToggleLoopRecord"), Colours.off
        )
