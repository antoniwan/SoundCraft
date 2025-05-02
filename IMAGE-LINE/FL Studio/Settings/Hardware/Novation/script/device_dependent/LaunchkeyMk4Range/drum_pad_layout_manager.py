from script.device_independent.view import DrumPadsView
from util.mapped_pad_led_writer import MappedPadLedWriter


class DrumPadLayoutManager:
    def __init__(self, action_dispatcher, pad_led_writer, product_defs, fl):
        self.action_dispatcher = action_dispatcher
        drum_pad_led_writer = MappedPadLedWriter(
            pad_led_writer, product_defs.Constants.NotesForPadLayout.value[product_defs.PadLayout.Drum]
        )
        self.views = {DrumPadsView(action_dispatcher, drum_pad_led_writer, fl, product_defs)}

    def show(self):
        for view in self.views:
            view.show()

    def hide(self):
        for view in self.views:
            view.hide()
