from script.constants import Encoders, Faders
from util.custom_enum import CustomEnum


class PadLayout(CustomEnum):
    ChannelRack = 2
    Drum = 15


class FaderLayout(CustomEnum):
    Volume = 1


class EncoderLayout(CustomEnum):
    Plugin = 2
    Mixer = 1
    Sends = 4
    Transport = 5


class Constants(CustomEnum):
    DisplayedDeviceName = "Launchkey MK4"

    NovationProductId = 0x14

    LightingTargetNote = 0x40
    LightingTargetCC = 0x50
    LightingTargetDrumrack = 0x60
    LightingTypeStatic = 0x00
    LightingTypeRGB = 0x03

    NotesForPadLayout = {
        PadLayout.ChannelRack: [96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116, 117, 118, 119],
        PadLayout.Drum: [40, 41, 42, 43, 48, 49, 50, 51, 36, 37, 38, 39, 44, 45, 46, 47],
    }
    PadForLayoutNote = {
        **{note: pad for pad, note in enumerate(NotesForPadLayout[PadLayout.ChannelRack])},
        **{note: pad for pad, note in enumerate(NotesForPadLayout[PadLayout.Drum])},
    }


class Button(CustomEnum):
    Shift = 0
    TrackLeft = 1
    TrackRight = 2
    TrackLeftShift = 3
    TrackRightShift = 4
    TransportPlay = 9
    TransportStop = 10
    TransportRecord = 11
    TransportLoop = 12
    CaptureMidi = 13
    Quantise = 14
    Undo = 15
    UndoShift = 16
    Metronome = 17
    Fader_1 = 21
    Fader_2 = 22
    Fader_3 = 23
    Fader_4 = 24
    Fader_5 = 25
    Fader_6 = 26
    Fader_7 = 27
    Fader_8 = 28
    ArmSelect = 29
    EncoderPageUp = 30
    EncoderPageDown = 31
    PadsPageUp = 32
    PadsPageDown = 33


class SurfaceEvent(CustomEnum):
    EnterDawMode = 0x9F, 0x0C, 0x7F
    ExitDawMode = 0x9F, 0x0C, 0x00
    TakeOwnershipOfDrumrack = 0xB6, 0x54, 0x7F
    ReleaseOwnershipOfDrumrack = 0xB6, 0x54, 0x0
    PadLayout = 0xB6, 0x1D
    LegacyPadLayout = 0xB6, 0x40
    EncoderLayout = 0xB6, 0x1E
    LegacyEncoderLayout = 0xB6, 0x41
    FaderLayout = 0xB6, 0x1F
    LegacyFaderLayout = 0xB6, 0x42
    FaderFirst = 0xBF, 0x05
    FaderLast = 0xBF, 0x0D
    EncoderFirst = 0xBF, 0x55
    EncoderLast = 0xBF, 0x5C
    ButtonTrackRight = 0xB0, 0x66
    ButtonTrackLeft = 0xB0, 0x67
    ButtonTrackRightShift = 0xB0, 0x6C
    ButtonTrackLeftShift = 0xB0, 0x6D
    ButtonTransportPlay = 0xB0, 0x73
    ButtonTransportStop = 0xB0, 0x74
    ButtonTransportRecord = 0xB0, 0x75
    ButtonTransportLoop = 0xB0, 0x76
    ButtonCaptureMidi = 0xB0, 0x4A
    ButtonQuantise = 0xB0, 0x4B
    ButtonMetronome = 0xB0, 0x4C
    ButtonUndo = 0xB0, 0x4D
    ButtonShift = 0xB6, 0x3F
    LegacyButtonShift = 0xB6, 0x48
    ButtonFader_1 = 0xB0, 0x25
    ButtonFader_2 = 0xB0, 0x26
    ButtonFader_3 = 0xB0, 0x27
    ButtonFader_4 = 0xB0, 0x28
    ButtonFader_5 = 0xB0, 0x29
    ButtonFader_6 = 0xB0, 0x2A
    ButtonFader_7 = 0xB0, 0x2B
    ButtonFader_8 = 0xB0, 0x2C
    ButtonArmSelect = 0xB0, 0x2D
    ButtonEncoderPageUp = 0xB0, 0x33
    ButtonEncoderPageDown = 0xB0, 0x34
    ButtonPadsPageUp = 0xB0, 0x6A
    ButtonPadsPageDown = 0xB0, 0x6B


class DisplayAddress(CustomEnum):
    Permanent = 0x20
    Overlay = 0x21
    FirstEncoder = 0x15
    LastEncoder = 0x1C
    FirstFader = 0x05
    LastFader = 0x0C


FunctionToButton = {
    "PreviewModifier": Button.Shift,
    "ShiftModifier": Button.Shift,
    "ShowHighlights": Button.Shift,
    "SelectPreviousMixerTrack": Button.TrackLeftShift,
    "SelectNextMixerTrack": Button.TrackRightShift,
    "MixerBankLeft": Button.TrackLeft,
    "MixerBankRight": Button.TrackRight,
    "SelectPreviousChannel": Button.PadsPageUp,
    "SelectNextChannel": Button.PadsPageDown,
    "ToggleLoopRecord": Button.TransportLoop,
    "ToggleMetronome": Button.Metronome,
    "TransportTogglePlayPause": Button.TransportPlay,
    "TransportStop": Button.TransportStop,
    "TransportToggleRecording": Button.TransportRecord,
    "DumpScoreLog": Button.CaptureMidi,
    "Quantise": Button.Quantise,
    "Undo": Button.Undo,
    "Redo": Button.UndoShift,
    "SelectNextMixerEncoderMode": Button.EncoderPageUp,
    "SelectPreviousMixerEncoderMode": Button.EncoderPageDown,
    "ToggleArmMute_1": Button.Fader_1,
    "ToggleArmMute_2": Button.Fader_2,
    "ToggleArmMute_3": Button.Fader_3,
    "ToggleArmMute_4": Button.Fader_4,
    "ToggleArmMute_5": Button.Fader_5,
    "ToggleArmMute_6": Button.Fader_6,
    "ToggleArmMute_7": Button.Fader_7,
    "ToggleArmMute_8": Button.Fader_8,
    "ArmSelect": Button.ArmSelect,
}

ButtonToLedIndex = {
    Button.Fader_1: 0x25,
    Button.Fader_2: 0x26,
    Button.Fader_3: 0x27,
    Button.Fader_4: 0x28,
    Button.Fader_5: 0x29,
    Button.Fader_6: 0x2A,
    Button.Fader_7: 0x2B,
    Button.Fader_8: 0x2C,
    Button.ArmSelect: 0x2D,
    Button.CaptureMidi: 0x4A,
    Button.Quantise: 0x4B,
    Button.Metronome: 0x4C,
    Button.TrackRight: 0x66,
    Button.TrackLeft: 0x67,
    Button.TrackRightShift: 0x6C,
    Button.TrackLeftShift: 0x6D,
    Button.TransportPlay: 0x73,
    Button.TransportStop: 0x74,
    Button.TransportRecord: 0x75,
    Button.TransportLoop: 0x76,
    Button.Undo: 0x4D,
    Button.UndoShift: 0x4D,
    Button.EncoderPageUp: 0x33,
    Button.EncoderPageDown: 0x34,
    Button.PadsPageUp: 0x6A,
    Button.PadsPageDown: 0x6B,
}

EncoderIndexToControlIndex = {
    index: Encoders.FirstControlIndex.value + control for index, control in enumerate(range(Encoders.Num.value))
}

FaderIndexToControlIndex = {
    index: Faders.FirstControlIndex.value + control for index, control in enumerate(range(Faders.Num.value))
}


class LaunchkeyMk4ProductDefs:
    def __init__(self):
        self.Constants = Constants
        self.Button = Button
        self.PadLayout = PadLayout
        self.FaderLayout = FaderLayout
        self.EncoderLayout = EncoderLayout
        self.SurfaceEvent = SurfaceEvent
        self.DisplayAddress = DisplayAddress
        self.FunctionToButton = FunctionToButton
        self.ButtonToLedIndex = ButtonToLedIndex
        self.EncoderIndexToControlIndex = EncoderIndexToControlIndex
        self.ControlIndexToEncoderIndex = {v: k for k, v in self.EncoderIndexToControlIndex.items()}
        self.FaderIndexToControlIndex = FaderIndexToControlIndex
        self.ControlIndexToFaderIndex = {v: k for k, v in self.FaderIndexToControlIndex.items()}

    def IsShiftButton(self, button):
        return button in [Button.UndoShift, Button.TrackRightShift, Button.TrackLeftShift]

    def ForwardButtonLedGivenShift(self, button, shift_pressed):
        return self.IsShiftButton(button) == shift_pressed
