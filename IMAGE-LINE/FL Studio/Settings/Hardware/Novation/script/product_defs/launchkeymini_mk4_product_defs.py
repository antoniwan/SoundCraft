from script.constants import Encoders
from util.custom_enum import CustomEnum


class PadLayout(CustomEnum):
    ChannelRack = 2
    Drum = 15


class EncoderLayout(CustomEnum):
    Plugin = 2
    Mixer = 1
    Sends = 4
    Transport = 5


class Constants(CustomEnum):
    DisplayedDeviceName = "Launchkey Mini MK4"

    NovationProductId = 0x13

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
    TransportPlay = 9
    TransportPlayShift = 10
    TransportRecord = 11
    TransportRecordShift = 12
    EncoderPageUp = 30
    EncoderPageDown = 31
    PadsPageUp = 32
    PadsPageDown = 33
    PadsPageUpShift = 34
    PadsPageDownShift = 35


class SurfaceEvent(CustomEnum):
    EnterDawMode = 0x9F, 0x0C, 0x7F
    ExitDawMode = 0x9F, 0x0C, 0x00
    TakeOwnershipOfDrumrack = 0xB6, 0x54, 0x7F
    ReleaseOwnershipOfDrumrack = 0xB6, 0x54, 0x00
    PadLayout = 0xB6, 0x1D
    LegacyPadLayout = 0xB6, 0x40
    EncoderLayout = 0xB6, 0x1E
    LegacyEncoderLayout = 0xB6, 0x41
    EncoderFirst = 0xBF, 0x55
    EncoderLast = 0xBF, 0x5C
    ButtonTransportPlay = 0xB0, 0x73
    ButtonTransportRecord = 0xB0, 0x75
    ButtonShift = 0xB6, 0x3F
    LegacyButtonShift = 0xB6, 0x48
    ButtonEncoderPageUp = 0xB0, 0x33
    ButtonEncoderPageDown = 0xB0, 0x34
    ButtonPadsPageUp = 0xB0, 0x6A
    ButtonPadsPageDown = 0xB0, 0x6B
    ButtonPadsPageUpShift = 0xB0, 0x66
    ButtonPadsPageDownShift = 0xB0, 0x67


class DisplayAddress(CustomEnum):
    Permanent = 0x20
    Overlay = 0x21
    FirstEncoder = 0x15
    LastEncoder = 0x1C
    FirstFader = 0x05
    LastFader = 0x0C


FunctionToButton = {
    "ShiftModifier": Button.Shift,
    "ShowHighlights": Button.Shift,
    "SelectPreviousChannel": Button.PadsPageUp,
    "SelectNextChannel": Button.PadsPageDown,
    "MixerBankLeft": Button.PadsPageUpShift,
    "MixerBankRight": Button.PadsPageDownShift,
    "TransportTogglePlayStop": Button.TransportPlay,
    "TransportPause": Button.TransportPlayShift,
    "TransportToggleRecording": Button.TransportRecord,
    "DumpScoreLog": Button.TransportRecordShift,
    "SelectNextMixerEncoderMode": Button.EncoderPageUp,
    "SelectPreviousMixerEncoderMode": Button.EncoderPageDown,
}

ButtonToLedIndex = {
    Button.TransportPlay: 0x73,
    Button.TransportPlayShift: 0x73,
    Button.TransportRecord: 0x75,
    Button.TransportRecordShift: 0x75,
    Button.EncoderPageUp: 0x33,
    Button.EncoderPageDown: 0x34,
    Button.PadsPageUp: 0x6A,
    Button.PadsPageDown: 0x6B,
    Button.PadsPageUpShift: 0x66,
    Button.PadsPageDownShift: 0x67,
}

EncoderIndexToControlIndex = {
    index: Encoders.FirstControlIndex.value + control for index, control in enumerate(range(Encoders.Num.value))
}


class LaunchkeyMiniMk4ProductDefs:
    def __init__(self):
        self.Constants = Constants
        self.Button = Button
        self.PadLayout = PadLayout
        self.EncoderLayout = EncoderLayout
        self.SurfaceEvent = SurfaceEvent
        self.DisplayAddress = DisplayAddress
        self.FunctionToButton = FunctionToButton
        self.ButtonToLedIndex = ButtonToLedIndex
        self.EncoderIndexToControlIndex = EncoderIndexToControlIndex
        self.ControlIndexToEncoderIndex = {v: k for k, v in self.EncoderIndexToControlIndex.items()}

    def IsShiftButton(self, button):
        return button in [
            Button.TransportPlayShift,
            Button.TransportRecordShift,
            Button.PadsPageUpShift,
            Button.PadsPageDownShift,
        ]

    def ForwardButtonLedGivenShift(self, button, shift_pressed):
        return self.IsShiftButton(button) == shift_pressed
