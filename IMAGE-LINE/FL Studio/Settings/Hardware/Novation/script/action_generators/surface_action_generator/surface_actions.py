from script.constants import FaderArmMuteMode, FaderMuteSelectMode, FaderSoloArmMode
from util.custom_enum import CustomEnum
from util.plain_data import PlainData


@PlainData
class ArmSelectStateChangedAction:
    mode: FaderArmMuteMode


@PlainData
class SoloArmStateChangedAction:
    mode: FaderSoloArmMode


@PlainData
class MuteSelectStateChangedAction:
    mode: FaderMuteSelectMode


@PlainData
class ChannelMuteModeAction:
    pass


@PlainData
class ChannelSelectModeAction:
    pass


@PlainData
class PadLayoutChangedAction:
    layout: CustomEnum


@PlainData
class ControlChangedAction:
    control_change_type: CustomEnum
    control: int
    value: float


@PlainData
class PotLayoutChangedAction:
    layout: CustomEnum


@PlainData
class FaderLayoutChangedAction:
    layout: CustomEnum


@PlainData
class EncoderLayoutChangedAction:
    layout: CustomEnum


@PlainData
class DeviceLayoutChangedAction:
    layout: CustomEnum


@PlainData
class PadPressAction:
    pad: int
    velocity: int


@PlainData
class PadReleaseAction:
    pad: int


@PlainData
class ButtonPressedAction:
    button: CustomEnum


@PlainData
class ButtonReleasedAction:
    button: CustomEnum


@PlainData
class ScaleEnabledAction:
    pass


@PlainData
class ScaleDisabledAction:
    pass


@PlainData
class ScaleTypeChangedAction:
    scale_index: int


@PlainData
class ScaleRootChangedAction:
    scale_root: int


@PlainData
class SurfaceInteractionDiscardedAction:
    discarded_action: PlainData
