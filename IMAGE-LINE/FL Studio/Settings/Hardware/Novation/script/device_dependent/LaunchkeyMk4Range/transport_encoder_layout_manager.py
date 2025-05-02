from script.device_independent.view import (
    NotUsedPreviewView,
    TransportIdleScreenView,
    TransportMarkerPreviewView,
    TransportMarkerScreenView,
    TransportMarkerView,
    TransportSongPositionPreviewView,
    TransportSongPositionScreenView,
    TransportSongPositionView,
    TransportTempoPreviewView,
    TransportTempoScreenView,
    TransportTempoView,
    TransportZoomPreviewView,
    TransportZoomScreenView,
    TransportZoomView,
)


class TransportEncoderLayoutManager:
    def __init__(self, action_dispatcher, fl, screen_writer, device_manager, product_defs):
        self.device_manager = device_manager
        encoders = {
            **{index: product_defs.EncoderIndexToControlIndex.get(encoder) for index, encoder in enumerate(range(8))},
        }
        self.views = [
            TransportSongPositionView(action_dispatcher, fl, control_index=encoders[0]),
            TransportSongPositionScreenView(action_dispatcher, fl, screen_writer, control_index=encoders[0]),
            TransportSongPositionPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[0]),
            TransportZoomView(action_dispatcher, fl, control_index=encoders[1]),
            TransportZoomScreenView(action_dispatcher, screen_writer, control_index=encoders[1]),
            TransportZoomPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[1]),
            TransportMarkerView(action_dispatcher, fl, control_index=encoders[4]),
            TransportMarkerScreenView(action_dispatcher, screen_writer, control_index=encoders[4]),
            TransportMarkerPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[4]),
            TransportTempoView(action_dispatcher, fl, control_index=encoders[7]),
            TransportTempoScreenView(action_dispatcher, fl, screen_writer, control_index=encoders[7]),
            TransportTempoPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[7]),
            TransportIdleScreenView(action_dispatcher, screen_writer),
            NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[2]),
            NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[3]),
            NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[5]),
            NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[6]),
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
