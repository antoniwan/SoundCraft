from util.custom_enum import CustomEnum
from util.plain_data import PlainData


class DeviceId(CustomEnum):
    FLkey37 = 0
    FLkeyMini = 1
    LaunchkeyMini = 2
    Launchkey = 3
    Launchkey88 = 4
    FLkey49 = 5
    FLkey61 = 6
    LaunchkeyMiniMk4 = 7
    LaunchkeyMk4 = 8
    LaunchControlXlMk3 = 9


class ValidationState(CustomEnum):
    Idle = 0
    InProgress = 1
    Success = 2
    Failure = 3


class Pads(CustomEnum):
    Num = 16


class Pots(CustomEnum):
    FirstControlIndex = 0
    Num = 8


class Encoders(CustomEnum):
    FirstControlIndex = 0
    Num = 8


class Faders(CustomEnum):
    FirstControlIndex = 100
    NumRegularFaders = 8
    MasterFaderIndex = 8
    Num = 9


class FaderArmMuteMode(CustomEnum):
    Arm = 0
    Mute = 1


class FaderSoloArmMode(CustomEnum):
    Solo = 0
    Arm = 1


class FaderMuteSelectMode(CustomEnum):
    Mute = 0
    Select = 1


class ControlChangeType(CustomEnum):
    Absolute = 0
    Relative = 1


class SoloMuteEditState(CustomEnum):
    SingleTrackSolo = 0
    SingleTrackSoloMomentary = 1
    Mute = 2
    Suspended = 3


class MixerSoloMuteMode(CustomEnum):
    Mute = 0
    Solo = 1


class ChannelSoloMuteMode(CustomEnum):
    Mute = 0
    Solo = 1


class PatternSelectBank(CustomEnum):
    StepsPerBankingIncrement = 8
    NumPerBank = 16


class ChannelNavigationSteps(CustomEnum):
    Bank = 8


class ChannelNavigationMode(CustomEnum):
    Single = 0
    Bank = 1


class Notes(CustomEnum):
    Default = 60
    Min = 0
    Max = 127


class HighlightDuration(CustomEnum):
    WithoutEnd = -1
    Default = 3000


class ScrollingSpeed(CustomEnum):
    Default = 0
    Slow = 1


class ButtonFunction(CustomEnum):
    Quantise = 0
    Undo = 1
    Redo = 2
    DumpScoreLog = 3
    TransportPause = 4


class LedLightingType(CustomEnum):
    Static = 0
    Pulsing = 1
    RGB = 2


class PatternSelectionMethod(CustomEnum):
    Explicit = 0
    ThroughNew = 1
    ThroughClone = 2


class ArrowButtonChangeDirection(CustomEnum):
    Decrement = 0
    Increment = 1


class SelectedSequencerStepState:
    def __init__(self, *, edited=False, toggled=False):
        self.edited = edited
        self.toggled = toggled


class SequencerStepEditGroup:
    def __init__(self):
        self.edited = False
        self._steps = []
        self.displayed_step_edit_parameter = StepEditParameters.Velocity.value.index

    def get_steps(self):
        return self._steps

    def add_step(self, step):
        self._steps.append(step)

    def remove_step(self, step):
        self._steps.remove(step)
        if len(self._steps) == 0:
            self.edited = False

    def remove_all_steps(self):
        self._steps.clear()
        self.edited = False


class SequencerStepEditState(CustomEnum):
    EditIdle = 0
    EditWaiting = 1
    EditQuick = 2
    EditLatch = 3


class PluginParameterType(CustomEnum):
    Plugin = 0
    Channel = 1


class StepEditParameters(CustomEnum):
    @PlainData
    class Parameter:
        index: int
        minimum: int
        maximum: int
        is_bipolar: bool

    Pitch = Parameter(index=0, minimum=30, maximum=90, is_bipolar=False)
    Velocity = Parameter(index=1, minimum=0, maximum=128, is_bipolar=False)
    Release = Parameter(index=2, minimum=0, maximum=128, is_bipolar=False)
    PitchFine = Parameter(index=3, minimum=0, maximum=240, is_bipolar=True)
    Pan = Parameter(index=4, minimum=0, maximum=128, is_bipolar=True)
    ModX = Parameter(index=5, minimum=0, maximum=255, is_bipolar=True)
    ModY = Parameter(index=6, minimum=0, maximum=255, is_bipolar=True)
    Shift = Parameter(index=7, minimum=0, maximum=23, is_bipolar=False)


class SysEx(CustomEnum):
    MessageHeader = [0x00, 0x20, 0x29, 0x02]
    DeviceEnquiryRequest = [0x7E, 0x7F, 0x06, 0x01]
    DeviceEnquiryResponseHeader = [0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29]


class DisplayPriority(CustomEnum):
    Title = 0
    Name = 1


class MixerEncoderMode(CustomEnum):
    ChannelRackVolume = 0
    ChannelRackPan = 1
    MixerVolume = 2
    MixerPan = 3
    MixerEQ = 4


class Zoom(CustomEnum):
    In = 1
    Out = -1


class EqParameter(CustomEnum):
    Gain = 0
    Frequency = 1


class EqBand(CustomEnum):
    LowShelf = 0
    Peaking = 1
    HighShelf = 2


PluginsWithExplicitlyDisabledPresetNavigation = {"Slicex"}

Scales = {
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "major": [0, 2, 4, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "minor_pentatonic": [0, 3, 5, 7, 10],
    "major_pentatonic": [0, 2, 4, 7, 9],
}
