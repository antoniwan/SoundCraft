from script.constants import Encoders, Faders
from util.custom_enum import CustomEnum


class DeviceLayout(CustomEnum):
    Mixer = 1
    Control = 2


class Constants(CustomEnum):
    DisplayedDeviceName = "Launch Control XL 3"

    NovationProductId = 0x15

    LightingTargetNote = 0x40
    LightingTargetCC = 0x50
    LightingTypeStatic = 0x00
    LightingTypeRGB = 0x03

    ChannelsPerBank = 8

    NumEncoders = 24
    EncoderCcOffset = 0x0D
    EncoderRow1FirstIndex = Encoders.FirstControlIndex.value
    EncoderRow2FirstIndex = Encoders.FirstControlIndex.value + 8
    EncoderRow3FirstIndex = Encoders.FirstControlIndex.value + 16

    EqControlFirstIndex = EncoderRow1FirstIndex
    PanControlFirstIndex = EncoderRow3FirstIndex
    PluginParameterFirstIndex = EncoderRow1FirstIndex


class Button(CustomEnum):
    EncodersPageUp = 1
    EncodersPageDown = 2
    TrackLeft = 3
    TrackRight = 4
    TrackLeftShift = 5
    TrackRightShift = 6
    TransportRecord = 7
    TransportPlay = 8
    TransportPlayShift = 9
    Shift = 10
    SoloArm = 11
    MuteSelect = 12
    Fader_1 = 13
    Fader_2 = 14
    Fader_3 = 15
    Fader_4 = 16
    Fader_5 = 17
    Fader_6 = 18
    Fader_7 = 19
    Fader_8 = 20
    Fader_9 = 21
    Fader_10 = 22
    Fader_11 = 23
    Fader_12 = 24
    Fader_13 = 25
    Fader_14 = 26
    Fader_15 = 26
    Fader_16 = 27


class SurfaceEvent(CustomEnum):
    EnterDawMode = 0x9F, 0x0C, 0x7F
    ExitDawMode = 0x9F, 0x0C, 0x00
    ButtonTrackLeft = 0xB0, 0x67
    ButtonTrackRight = 0xB0, 0x66
    ButtonTransportRecord = 0xB0, 0x76
    ButtonTransportPlay = 0xB0, 0x74
    ButtonShift = 0xB6, 0x3F
    DeviceLayout = 0xB6, 0x1E
    ButtonSoloArm = 0xB0, 0x41
    ButtonMuteSelect = 0xB0, 0x42
    EncoderFirst = 0xBF, 0x4D
    EncoderLast = 0xBF, 0x64
    FaderFirst = 0xBF, 0x05
    FaderLast = 0xBF, 0x0C
    ButtonFader_1 = 0xB0, 0x25
    ButtonFader_2 = 0xB0, 0x26
    ButtonFader_3 = 0xB0, 0x27
    ButtonFader_4 = 0xB0, 0x28
    ButtonFader_5 = 0xB0, 0x29
    ButtonFader_6 = 0xB0, 0x2A
    ButtonFader_7 = 0xB0, 0x2B
    ButtonFader_8 = 0xB0, 0x2C
    ButtonFader_9 = 0xB0, 0x2D
    ButtonFader_10 = 0xB0, 0x2E
    ButtonFader_11 = 0xB0, 0x2F
    ButtonFader_12 = 0xB0, 0x30
    ButtonFader_13 = 0xB0, 0x31
    ButtonFader_14 = 0xB0, 0x32
    ButtonFader_15 = 0xB0, 0x33
    ButtonFader_16 = 0xB0, 0x34


class DisplayAddress(CustomEnum):
    Permanent = 0x35
    Overlay = 0x36
    FirstEncoder = 0x0D
    LastEncoder = 0x24
    FirstFader = 0x05
    LastFader = 0x0C


FunctionToButton = {
    "SelectPreviousChannelBank": Button.TrackLeft,
    "SelectNextChannelBank": Button.TrackRight,
    "MixerBankLeft": Button.TrackLeft,
    "MixerBankRight": Button.TrackRight,
    "SelectPreviousChannel": Button.TrackLeftShift,
    "SelectNextChannel": Button.TrackRightShift,
    "SelectPreviousMixerTrack": Button.TrackLeftShift,
    "SelectNextMixerTrack": Button.TrackRightShift,
    "TransportTogglePlayStop": Button.TransportPlay,
    "TransportPause": Button.TransportPlayShift,
    "TransportToggleRecording": Button.TransportRecord,
    "ShiftModifier": Button.Shift,
    "ShowHighlights": Button.Shift,
    "ArmSelect": Button.SoloArm,
    "SoloArm": Button.SoloArm,
    "Solo": Button.SoloArm,
    "ChannelSelect": Button.SoloArm,
    "MuteSelect": Button.MuteSelect,
    "Mute": Button.MuteSelect,
    "TrackSelect": Button.MuteSelect,
    "ToggleArmMute_1": Button.Fader_1,
    "ToggleArmMute_2": Button.Fader_2,
    "ToggleArmMute_3": Button.Fader_3,
    "ToggleArmMute_4": Button.Fader_4,
    "ToggleArmMute_5": Button.Fader_5,
    "ToggleArmMute_6": Button.Fader_6,
    "ToggleArmMute_7": Button.Fader_7,
    "ToggleArmMute_8": Button.Fader_8,
    "ToggleSolo_1": Button.Fader_1,
    "ToggleSolo_2": Button.Fader_2,
    "ToggleSolo_3": Button.Fader_3,
    "ToggleSolo_4": Button.Fader_4,
    "ToggleSolo_5": Button.Fader_5,
    "ToggleSolo_6": Button.Fader_6,
    "ToggleSolo_7": Button.Fader_7,
    "ToggleSolo_8": Button.Fader_8,
    "ChannelSelect_1": Button.Fader_1,
    "ChannelSelect_2": Button.Fader_2,
    "ChannelSelect_3": Button.Fader_3,
    "ChannelSelect_4": Button.Fader_4,
    "ChannelSelect_5": Button.Fader_5,
    "ChannelSelect_6": Button.Fader_6,
    "ChannelSelect_7": Button.Fader_7,
    "ChannelSelect_8": Button.Fader_8,
    "ToggleMute_1": Button.Fader_9,
    "ToggleMute_2": Button.Fader_10,
    "ToggleMute_3": Button.Fader_11,
    "ToggleMute_4": Button.Fader_12,
    "ToggleMute_5": Button.Fader_13,
    "ToggleMute_6": Button.Fader_14,
    "ToggleMute_7": Button.Fader_15,
    "ToggleMute_8": Button.Fader_16,
    "TrackSelect_1": Button.Fader_9,
    "TrackSelect_2": Button.Fader_10,
    "TrackSelect_3": Button.Fader_11,
    "TrackSelect_4": Button.Fader_12,
    "TrackSelect_5": Button.Fader_13,
    "TrackSelect_6": Button.Fader_14,
    "TrackSelect_7": Button.Fader_15,
    "TrackSelect_8": Button.Fader_16,
}


ButtonToLedIndex = {
    Button.TrackLeft: 0x67,
    Button.TrackRight: 0x66,
    Button.TrackLeftShift: 0x67,
    Button.TrackRightShift: 0x66,
    Button.TransportPlay: 0x74,
    Button.TransportPlayShift: 0x74,
    Button.TransportRecord: 0x76,
    Button.SoloArm: 0x41,
    Button.MuteSelect: 0x42,
    Button.Fader_1: 0x25,
    Button.Fader_2: 0x26,
    Button.Fader_3: 0x27,
    Button.Fader_4: 0x28,
    Button.Fader_5: 0x29,
    Button.Fader_6: 0x2A,
    Button.Fader_7: 0x2B,
    Button.Fader_8: 0x2C,
    Button.Fader_9: 0x2D,
    Button.Fader_10: 0x2E,
    Button.Fader_11: 0x2F,
    Button.Fader_12: 0x30,
    Button.Fader_13: 0x31,
    Button.Fader_14: 0x32,
    Button.Fader_15: 0x33,
    Button.Fader_16: 0x34,
}


EncoderIndexToControlIndex = {
    index: Encoders.FirstControlIndex.value + control
    for index, control in enumerate(range(Constants.NumEncoders.value))
}


FaderIndexToControlIndex = {
    index: Faders.FirstControlIndex.value + control
    for index, control in enumerate(range(Faders.NumRegularFaders.value))
}


class LaunchControlXlMk3ProductDefs:
    def __init__(self):
        self.Constants = Constants
        self.Button = Button
        self.DeviceLayout = DeviceLayout
        self.SurfaceEvent = SurfaceEvent
        self.DisplayAddress = DisplayAddress
        self.FunctionToButton = FunctionToButton
        self.ButtonToLedIndex = ButtonToLedIndex
        self.EncoderIndexToControlIndex = EncoderIndexToControlIndex
        self.ControlIndexToEncoderIndex = {v: k for k, v in self.EncoderIndexToControlIndex.items()}
        self.FaderIndexToControlIndex = FaderIndexToControlIndex
        self.ControlIndexToFaderIndex = {v: k for k, v in self.FaderIndexToControlIndex.items()}

    def IsShiftButton(self, button):
        return button in [
            Button.TransportPlayShift,
            Button.TrackRightShift,
            Button.TrackLeftShift,
        ]

    def ForwardButtonLedGivenShift(self, button, shift_pressed):
        return self.IsShiftButton(button) == shift_pressed
