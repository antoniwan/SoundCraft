from script.action_generators.surface_action_generator.keyboard_controller_common import (
    KeyboardControllerCommonButtonActionGenerator,
    KeyboardControllerCommonDeviceLayoutActionGenerator,
    KeyboardControllerCommonEncoderActionGenerator,
    KeyboardControllerCommonFaderActionGenerator,
)


class LaunchControlXlMk3SurfaceActionGenerator:
    def __init__(self, product_defs):
        self.product_defs = product_defs
        self.event_type_to_button = {
            self.product_defs.SurfaceEvent.ButtonTrackRight.value: self.product_defs.Button.TrackRight,
            self.product_defs.SurfaceEvent.ButtonTrackLeft.value: self.product_defs.Button.TrackLeft,
            self.product_defs.SurfaceEvent.ButtonTransportPlay.value: self.product_defs.Button.TransportPlay,
            self.product_defs.SurfaceEvent.ButtonTransportRecord.value: self.product_defs.Button.TransportRecord,
            self.product_defs.SurfaceEvent.ButtonShift.value: self.product_defs.Button.Shift,
            self.product_defs.SurfaceEvent.ButtonSoloArm.value: self.product_defs.Button.SoloArm,
            self.product_defs.SurfaceEvent.ButtonMuteSelect.value: self.product_defs.Button.MuteSelect,
            self.product_defs.SurfaceEvent.ButtonFader_1.value: self.product_defs.Button.Fader_1,
            self.product_defs.SurfaceEvent.ButtonFader_2.value: self.product_defs.Button.Fader_2,
            self.product_defs.SurfaceEvent.ButtonFader_3.value: self.product_defs.Button.Fader_3,
            self.product_defs.SurfaceEvent.ButtonFader_4.value: self.product_defs.Button.Fader_4,
            self.product_defs.SurfaceEvent.ButtonFader_5.value: self.product_defs.Button.Fader_5,
            self.product_defs.SurfaceEvent.ButtonFader_6.value: self.product_defs.Button.Fader_6,
            self.product_defs.SurfaceEvent.ButtonFader_7.value: self.product_defs.Button.Fader_7,
            self.product_defs.SurfaceEvent.ButtonFader_8.value: self.product_defs.Button.Fader_8,
            self.product_defs.SurfaceEvent.ButtonFader_9.value: self.product_defs.Button.Fader_9,
            self.product_defs.SurfaceEvent.ButtonFader_10.value: self.product_defs.Button.Fader_10,
            self.product_defs.SurfaceEvent.ButtonFader_11.value: self.product_defs.Button.Fader_11,
            self.product_defs.SurfaceEvent.ButtonFader_12.value: self.product_defs.Button.Fader_12,
            self.product_defs.SurfaceEvent.ButtonFader_13.value: self.product_defs.Button.Fader_13,
            self.product_defs.SurfaceEvent.ButtonFader_14.value: self.product_defs.Button.Fader_14,
            self.product_defs.SurfaceEvent.ButtonFader_15.value: self.product_defs.Button.Fader_15,
            self.product_defs.SurfaceEvent.ButtonFader_16.value: self.product_defs.Button.Fader_16,
        }

        self.modified_event_type_to_button = {
            self.product_defs.SurfaceEvent.ButtonTrackLeft.value: self.product_defs.Button.TrackLeftShift,
            self.product_defs.SurfaceEvent.ButtonTrackRight.value: self.product_defs.Button.TrackRightShift,
            self.product_defs.SurfaceEvent.ButtonTransportPlay.value: self.product_defs.Button.TransportPlayShift,
        }

        self.common_action_generators = [
            KeyboardControllerCommonButtonActionGenerator(
                self._get_button_for_event,
                is_modifier_event=lambda event: event == product_defs.SurfaceEvent.ButtonShift.value,
            ),
            KeyboardControllerCommonFaderActionGenerator(product_defs),
            KeyboardControllerCommonDeviceLayoutActionGenerator(product_defs),
            KeyboardControllerCommonEncoderActionGenerator(product_defs),
        ]

    def handle_midi_event(self, fl_event):
        for action_generator in self.common_action_generators:
            if actions := action_generator.handle_midi_event(fl_event):
                return actions
        return []

    def _get_button_for_event(self, event, modifier_button_is_held):
        if event == self.product_defs.SurfaceEvent.ButtonShift.value:
            return self.product_defs.Button.Shift
        if modifier_button_is_held:
            return self.modified_event_type_to_button.get(event)
        return self.event_type_to_button.get(event)
