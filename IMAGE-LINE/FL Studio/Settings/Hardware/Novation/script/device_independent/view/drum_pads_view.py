from script.colours import Colours
from script.constants import Pads
from script.device_independent.util_view.view import View
from script.fl_constants import RefreshFlags


class DrumPadsView(View):
    note_offset_for_pad = [40, 41, 42, 43, 48, 49, 50, 51, 36, 37, 38, 39, 44, 45, 46, 47]

    def __init__(self, action_dispatcher, pad_led_writer, fl, product_defs):
        super().__init__(action_dispatcher)
        self.pad_led_writer = pad_led_writer
        self.fl = fl
        self.product_defs = product_defs

    def _on_show(self):
        self._update_leds()

    def _on_hide(self):
        self._turn_off_leds()

    def handle_ChannelSelectAction(self, action):
        self._update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.ChannelSelection.value or action.flags & RefreshFlags.LedUpdate.value:
            self._update_leds()

    def handle_PadPressAction(self, action):
        note = self.note_offset_for_pad[action.pad]
        self.fl.send_note_on(note, action.velocity)

    def handle_PadReleaseAction(self, action):
        note = self.note_offset_for_pad[action.pad]
        self.fl.send_note_off(note)

    def _update_leds(self):
        colour = self.fl.get_channel_colour() if self.fl.is_any_channel_selected() else Colours.off
        for pad in range(Pads.Num.value):
            self.pad_led_writer.set_pad_colour(
                pad, colour, target=self.product_defs.Constants.LightingTargetDrumrack.value
            )

    def _turn_off_leds(self):
        for pad in range(Pads.Num.value):
            self.pad_led_writer.set_pad_colour(
                pad, Colours.off, target=self.product_defs.Constants.LightingTargetDrumrack.value
            )
