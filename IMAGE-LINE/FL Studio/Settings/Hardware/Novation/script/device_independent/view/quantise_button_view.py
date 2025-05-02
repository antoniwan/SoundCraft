from script.actions import FunctionTriggeredAction
from script.colours import Colours
from script.constants import ButtonFunction
from script.device_independent.util_view.single_button_view import SingleButtonView
from script.device_independent.util_view.view import View


class QuantiseButtonView(View):
    def __init__(self, action_dispatcher, button_led_writer, fl, product_defs):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.product_defs = product_defs
        self.button_view = SingleButtonView(button_led_writer, product_defs, "Quantise", available_colour=Colours.off)

    def _on_show(self):
        self.button_view.show()

    def _on_hide(self):
        self.button_view.hide()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("Quantise"):
            self.fl.quantise_start_only()
            self.action_dispatcher.dispatch(FunctionTriggeredAction(function=ButtonFunction.Quantise))
            self.button_view.set_pressed()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("Quantise"):
            self.button_view.set_not_pressed()
