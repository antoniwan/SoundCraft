from script.actions import FunctionTriggeredAction
from script.colours import Colours
from script.constants import ButtonFunction
from script.device_independent.util_view import SingleButtonView, View


class DumpScoreLogButtonView(View):
    default_dump_score_log_duration_in_minutes = 5
    default_dump_score_log_duration_in_seconds = default_dump_score_log_duration_in_minutes * 60

    def __init__(self, action_dispatcher, button_led_writer, fl, product_defs):
        super().__init__(action_dispatcher)
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.product_defs = product_defs
        self.button_view = SingleButtonView(
            button_led_writer, product_defs, "DumpScoreLog", available_colour=Colours.off
        )

    def _on_show(self):
        self.button_view.show()

    def _on_hide(self):
        self.button_view.hide()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("DumpScoreLog"):
            self.fl.dump_score_log(self.default_dump_score_log_duration_in_seconds)
            self.action_dispatcher.dispatch(FunctionTriggeredAction(function=ButtonFunction.DumpScoreLog))
            self.button_view.set_pressed()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("DumpScoreLog"):
            self.button_view.set_not_pressed()
