from script.constants import DeviceId
from script.device_adapters.device_manager.launchcontrolxl_mk3_device_manager import LaunchControlXlMk3DeviceManager
from script.device_adapters.device_manager.launchkey_mk4_range_device_manager import LaunchkeyMk4RangeDeviceManager

from .flkeyrange_device_manager import FLKeyRangeDeviceManager

__all__ = ["make_device_manager"]

from .launchkey_device_manager import LaunchkeyDeviceManager


def make_device_manager(device_id, sender, product_defs):
    """Instantiates and returns the relevant implementation of DeviceManager.

    Args:
        device_id: Device for which to return an implementation of DeviceManager.
        sender: required by DeviceManager instance to control hardware.
        product_defs: required by DeviceManager to send device specific control messages.

    Returns:
        Instance of a DeviceManager implementation.
    """
    if device_id in [DeviceId.FLkey37, DeviceId.FLkey49, DeviceId.FLkey61, DeviceId.FLkeyMini]:
        return FLKeyRangeDeviceManager(sender, product_defs)
    if device_id in [DeviceId.Launchkey, DeviceId.Launchkey88]:
        return LaunchkeyDeviceManager(sender, product_defs)
    if device_id in [DeviceId.LaunchkeyMk4, DeviceId.LaunchkeyMiniMk4]:
        return LaunchkeyMk4RangeDeviceManager(sender, product_defs)
    if device_id == DeviceId.LaunchControlXlMk3:
        return LaunchControlXlMk3DeviceManager(sender, product_defs)
    return None
