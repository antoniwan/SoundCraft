from util.custom_enum import CustomEnum


class FlConstants(CustomEnum):
    MaxStepsPerPattern = 512
    FirstPatternIndex = 1
    MasterTrackIndex = 0
    NumMixerEffectPluginSlots = 10


class ChannelType(CustomEnum):
    Sampler = 0
    Hybrid = 1
    Generator = 2
    Layer = 3
    AudioClip = 4
    AutomationClip = 5


class InstrumentPlugin(CustomEnum):
    Fpc = "FPC"
    FruitySlicer = "Fruity Slicer"
    SliceX = "Slicex"


class PluginType(CustomEnum):
    Instrument = 0
    Effect = 1


class DockSide(CustomEnum):
    Left = 0
    Center = 1
    Right = 2


class RefreshFlags(CustomEnum):
    MixerSelection = 1
    MixerControls = 4
    RemoteLinks = 16
    ChannelSelection = 32
    PerformanceLayout = 64
    TransportStatus = 256
    LedUpdate = 256
    Pattern = 1024
    PluginValue = 4096
    PluginColours = 8192
    PluginNames = 16384
    ChannelGroup = 32768
    ChannelEvent = 65536


class UndoType(CustomEnum):
    PianoRoll = 2


class DirtyChannelUpdateType(CustomEnum):
    New = 0
    Delete = 1
    Replace = 2
    Rename = 3
    Select = 4


class DirtyMixerTrackFlags(CustomEnum):
    AllTracksChanged = -1


class GlobalTransportCommand(CustomEnum):
    Play = 10
    Stop = 11
    Record = 12
    TapTempoEvent = 106
    Metronome = 110
    LoopRecord = 113


class LoopMode(CustomEnum):
    Pattern = 0
    Song = 1


class SlicexNoteRange(CustomEnum):
    Min = 0
    Max = 124


class PickupFollowMode(CustomEnum):
    NoPickup = 0
    UsePickup = 1
    FollowUserSetting = 2


class ProjectLoadStatus(CustomEnum):
    LoadStart = 0
    LoadFinished = 100
    LoadFailed = 101


class WindowType(CustomEnum):
    Mixer = 0
    ChannelRack = 1
    Playlist = 2
    PianoRoll = 3
    Browser = 4
    Plugin = 5
    PluginEffect = 6
    PluginGenerator = 7


class ChannelRackDisplayFlags(CustomEnum):
    Steps = 0
    ScrollToView = 2
    Mute = 4
    PanAndVolume = 8
    TrackSend = 16
    Name = 32
    Select = 64


class PatternGroups(CustomEnum):
    AllPatterns = -1


class PluginChannelParameterIndex(CustomEnum):
    FilterCutoff = 2
    FilterResonance = 3
    FilterType = 5
    GateTime = 9
    TimeShift = 11
    SwingMix = 12
    SampleStart = 13
    BipolarFilterCutoff = 19
    BipolarFilterResonance = 20


PluginChannelParameterValueRange = {
    PluginChannelParameterIndex.FilterCutoff.value: (0, 256),
    PluginChannelParameterIndex.FilterResonance.value: (0, 256),
    PluginChannelParameterIndex.FilterType.value: (0, 7),
    PluginChannelParameterIndex.GateTime.value: (0, 1447),
    PluginChannelParameterIndex.TimeShift.value: (0, 1024),
    PluginChannelParameterIndex.SwingMix.value: (0, 128),
    PluginChannelParameterIndex.SampleStart.value: (0, 16384),
    PluginChannelParameterIndex.BipolarFilterCutoff.value: (-256, 256),
    PluginChannelParameterIndex.BipolarFilterResonance.value: (-256, 256),
}


class EqRange(CustomEnum):
    MaxGain = 1800
    MaxFrequency = 65536
