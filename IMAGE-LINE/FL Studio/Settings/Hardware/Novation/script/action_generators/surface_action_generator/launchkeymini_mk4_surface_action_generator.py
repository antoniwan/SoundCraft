from script.action_generators.surface_action_generator.keyboard_controller_common import (
    KeyboardControllerCommonButtonActionGenerator,
    KeyboardControllerCommonEncoderActionGenerator,
    KeyboardControllerCommonEncoderLayoutActionGenerator,
    KeyboardControllerCommonPadActionGenerator,
    KeyboardControllerCommonPadLayoutActionGenerator,
)
from script.action_generators.surface_action_generator.surface_actions import (
    EncoderLayoutChangedAction,
    PadLayoutChangedAction,
)


class LaunchkeyMiniMk4SurfaceActionGenerator:
    def __init__(self, product_defs):
        self.product_defs = product_defs
        self.event_type_to_button = {
            self.product_defs.SurfaceEvent.ButtonTransportPlay.value: self.product_defs.Button.TransportPlay,
            self.product_defs.SurfaceEvent.ButtonTransportRecord.value: self.product_defs.Button.TransportRecord,
            self.product_defs.SurfaceEvent.ButtonShift.value: self.product_defs.Button.Shift,
            self.product_defs.SurfaceEvent.LegacyButtonShift.value: self.product_defs.Button.Shift,
            self.product_defs.SurfaceEvent.ButtonEncoderPageUp.value: self.product_defs.Button.EncoderPageUp,
            self.product_defs.SurfaceEvent.ButtonEncoderPageDown.value: self.product_defs.Button.EncoderPageDown,
            self.product_defs.SurfaceEvent.ButtonPadsPageUp.value: self.product_defs.Button.PadsPageUp,
            self.product_defs.SurfaceEvent.ButtonPadsPageDown.value: self.product_defs.Button.PadsPageDown,
        }

        self.modified_event_type_to_button = {
            self.product_defs.SurfaceEvent.ButtonTransportPlay.value: self.product_defs.Button.TransportPlayShift,
            self.product_defs.SurfaceEvent.ButtonTransportRecord.value: self.product_defs.Button.TransportRecordShift,
            self.product_defs.SurfaceEvent.ButtonPadsPageUpShift.value: self.product_defs.Button.PadsPageUpShift,
            self.product_defs.SurfaceEvent.ButtonPadsPageDownShift.value: self.product_defs.Button.PadsPageDownShift,
        }

        self.common_action_generators = [
            KeyboardControllerCommonButtonActionGenerator(
                self._get_button_for_event,
                is_modifier_event=lambda event: event == product_defs.SurfaceEvent.ButtonShift.value
                or event == product_defs.SurfaceEvent.LegacyButtonShift.value,
            ),
            KeyboardControllerCommonEncoderActionGenerator(product_defs),
            KeyboardControllerCommonPadActionGenerator(product_defs),
            KeyboardControllerCommonPadLayoutActionGenerator(product_defs),
            KeyboardControllerCommonEncoderLayoutActionGenerator(product_defs),
        ]

    def handle_midi_event(self, fl_event):
        for action_generator in self.common_action_generators:
            if actions := action_generator.handle_midi_event(fl_event):
                return actions
        if actions := self._handle_legacy_message(fl_event):
            return actions
        return []

    def _get_button_for_event(self, event, modifier_button_is_held):
        if (
            event == self.product_defs.SurfaceEvent.ButtonShift.value
            or event == self.product_defs.SurfaceEvent.LegacyButtonShift.value
        ):
            return self.product_defs.Button.Shift
        if modifier_button_is_held:
            return self.modified_event_type_to_button.get(event)
        return self.event_type_to_button.get(event)

    def _handle_legacy_message(self, fl_event):
        event_type = fl_event.status, fl_event.data1
        if event_type == self.product_defs.SurfaceEvent.LegacyPadLayout.value:
            return [PadLayoutChangedAction(layout=fl_event.data2)]
        if event_type == self.product_defs.SurfaceEvent.LegacyEncoderLayout.value:
            return [EncoderLayoutChangedAction(layout=fl_event.data2)]
        return []
