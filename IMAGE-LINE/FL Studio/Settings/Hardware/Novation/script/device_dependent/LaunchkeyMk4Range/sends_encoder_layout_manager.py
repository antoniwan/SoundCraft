from script.constants import Encoders
from script.device_independent.view import NotUsedPreviewView


class SendsEncoderLayoutManager:
    def __init__(self, action_dispatcher, screen_writer, device_manager, product_defs):
        self.device_manager = device_manager
        self.screen_writer = screen_writer
        encoders = {
            **{
                index: product_defs.EncoderIndexToControlIndex.get(encoder)
                for index, encoder in enumerate(range(Encoders.Num.value))
            },
        }
        self.views = [
            NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[index])
            for index in range(Encoders.Num.value)
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
