from script.actions import FunctionTriggeredAction
from script.colours import Colours
from script.constants import ButtonFunction
from script.device_independent.util_view import SingleButtonView, View


class RedoButtonView(View):
    def __init__(self, action_dispatcher, button_led_writer, fl, product_defs):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.product_defs = product_defs
        self.button_view = SingleButtonView(button_led_writer, product_defs, "Redo", available_colour=Colours.off)

    def _on_show(self):
        self.button_view.show()

    def _on_hide(self):
        self.button_view.hide()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.button_view.button:
            self.fl.redo()
            self.action_dispatcher.dispatch(FunctionTriggeredAction(function=ButtonFunction.Redo))
            self.button_view.set_pressed()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.button_view.button:
            self.button_view.set_not_pressed()
