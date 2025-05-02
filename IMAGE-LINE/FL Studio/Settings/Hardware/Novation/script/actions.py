from script.constants import ButtonFunction, PatternSelectionMethod, StepEditParameters
from util.plain_data import PlainData

"""
Actions are broadcast to all interested subscribers. Actions should
be named with past-tense phrases like "PresetChangedAction".
Actions convey that something has happened.
"""


@PlainData
class FpcBankAction:
    pass


@PlainData
class SequencerPageChangedAction:
    pass


@PlainData
class SequencerPageChangeAttemptedAction:
    pass


@PlainData
class SequencerPageResetAction:
    pass


@PlainData
class DefaultOctaveChangedAction:
    pass


@PlainData
class SlicerPluginBankAction:
    pass


@PlainData
class ChannelSelectAction:
    pass


@PlainData
class FlGuiChannelSelectAction:
    pass


@PlainData
class ChannelSelectAttemptedAction:
    pass


@PlainData
class ChannelRackNavigationModeChangedAction:
    pass


@PlainData
class MixerTrackSelectedAction:
    pass


@PlainData
class MixerTrackPluginSelectedAction:
    pass


@PlainData
class MixerBankChangedAction:
    pass


@PlainData
class MixerBankChangeAttemptedAction:
    pass


@PlainData
class ChannelBankChangedAction:
    pass


@PlainData
class ChannelBankChangeAttemptedAction:
    pass


@PlainData
class MixerTrackVolumeChangedAction:
    track: int
    control: int


@PlainData
class MixerTrackVolumePreviewedAction:
    track: int
    control: int


@PlainData
class MixerTrackPanChangedAction:
    track: int
    control: int
    value: float


@PlainData
class MixerTrackEqChangedAction:
    control: int
    band: int
    parameter: int


@PlainData
class MixerTrackEqPreviewedAction:
    control: int
    band: int
    parameter: int


@PlainData
class MixerTrackPanPreviewedAction:
    track: int
    control: int
    value: float


@PlainData
class ChannelVolumeChangedAction:
    channel: int
    control: int


@PlainData
class ChannelVolumePreviewedAction:
    channel: int
    control: int


@PlainData
class ChannelPanChangedAction:
    channel: int
    control: int
    value: float


@PlainData
class ChannelPanPreviewedAction:
    channel: int
    control: int
    value: float


@PlainData
class PresetChangedAction:
    pass


@PlainData
class PluginParameterValueChangedAction:
    parameter: int
    control: int
    value = None


@PlainData
class PluginParameterValuePreviewedAction:
    parameter: int
    control: int
    value = None


class ShowHighlightsAction:
    pass


@PlainData
class HideHighlightsAction:
    pass


@PlainData
class SequencerStepPressAction:
    step: int


@PlainData
class SequencerStepReleaseAction:
    step: int


@PlainData
class SequencerStepEditGroupChangedAction:
    pass


@PlainData
class SequencerStepEditStateChangedAction:
    pass


@PlainData
class SequencerStepEditParameterChangedAction:
    control: int
    parameter: StepEditParameters.Parameter
    value: int


@PlainData
class SequencerStepEditParameterChangeAttemptedAction:
    parameter: StepEditParameters.Parameter


@PlainData
class ScaleModelChangedAction:
    pass


@PlainData
class TransportRecordStateChangedAction:
    pass


@PlainData
class TransportPlaybackStateChangedAction:
    pass


@PlainData
class MetronomeStateChangedAction:
    pass


@PlainData
class FunctionTriggeredAction:
    function: ButtonFunction


@PlainData
class DefaultInstrumentLayoutMappingChangedAction:
    pass


@PlainData
class MixerSoloStateChangedAction:
    track: int
    enabled: bool


@PlainData
class MixerMuteStateChangedAction:
    track: int
    enabled: bool


@PlainData
class ChannelSoloStateChangedAction:
    channel: int
    enabled: bool


@PlainData
class ChannelMuteStateChangedAction:
    channel: int
    enabled: bool


@PlainData
class MixerSoloMuteModeChangedAction:
    pass


@PlainData
class ChannelSoloMuteModeChangedAction:
    pass


@PlainData
class PatternSelectBankChangedAction:
    pass


@PlainData
class PatternSelectBankChangeAttemptedAction:
    pass


@PlainData
class PatternSelectedAction:
    method: PatternSelectionMethod


@PlainData
class SongPositionChangedAction:
    pass


@PlainData
class TempoChangedAction:
    pass


@PlainData
class HorZoomChangedAction:
    value: int
    control: int


@PlainData
class NextMarkerSelectedAction:
    pass


@PlainData
class PreviousMarkerSelectedAction:
    pass


@PlainData
class MarkerSelectBlockedAction:
    message: str
