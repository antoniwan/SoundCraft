from script.constants import DeviceId

from .keyboard_controller_screen_writer import KeyboardControllerScreenWriter
from .launchkey_mk4_range_screen_writer import LaunchkeyMk4RangeScreenWriter
from .screen_writer_wrapper import ScreenWriterWrapper

__all__ = ["make_screen_writer"]


def make_screen_writer(device_id, sender, product_defs):
    """Instantiates and returns the relevant implementation of ScreenWriter.

    Args:
        device_id: Device for which to return an implementation of ScreenWriter.
        sender: required by LedWriter instance to control hardware.

    Returns:
        Instance of a ScreenWriter implementation.
    """
    if device_id in [DeviceId.FLkey37, DeviceId.FLkey49, DeviceId.FLkey61]:
        return ScreenWriterWrapper(KeyboardControllerScreenWriter(sender, product_defs))
    if device_id in [DeviceId.Launchkey, DeviceId.Launchkey88]:
        return ScreenWriterWrapper(KeyboardControllerScreenWriter(sender, product_defs))
    if device_id in [DeviceId.LaunchkeyMk4, DeviceId.LaunchkeyMiniMk4, DeviceId.LaunchControlXlMk3]:
        return LaunchkeyMk4RangeScreenWriter(sender, product_defs)
    return ScreenWriterWrapper(None)
