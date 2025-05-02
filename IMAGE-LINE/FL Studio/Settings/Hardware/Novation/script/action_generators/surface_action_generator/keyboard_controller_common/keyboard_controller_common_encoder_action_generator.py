from script.action_generators.surface_action_generator.surface_actions import ControlChangedAction
from script.constants import ControlChangeType


class KeyboardControllerCommonEncoderActionGenerator:
    PivotValue = 64
    MaxMidiValue = 127

    def __init__(self, product_defs):
        self.product_defs = product_defs

    def handle_midi_event(self, fl_event):
        encoder_event_status, encoder_first_index = self.product_defs.SurfaceEvent.EncoderFirst.value
        _, encoder_last_index = self.product_defs.SurfaceEvent.EncoderLast.value
        if fl_event.status == encoder_event_status and encoder_first_index <= fl_event.data1 <= encoder_last_index:
            encoder = fl_event.data1 - encoder_first_index
            delta = (fl_event.data2 - self.PivotValue) / self.MaxMidiValue
            if (control := self.product_defs.EncoderIndexToControlIndex.get(encoder)) is not None:
                return [
                    ControlChangedAction(control_change_type=ControlChangeType.Relative, control=control, value=delta)
                ]
        return []
