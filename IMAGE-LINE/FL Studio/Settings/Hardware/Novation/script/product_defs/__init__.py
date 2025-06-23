from script.constants import DeviceId
from script.product_defs.flkey_product_defs import FLkeyProductDefs
from script.product_defs.flkeymini_product_defs import FLkeyMiniProductDefs
from script.product_defs.launchcontrolxl_mk3_product_defs import LaunchControlXlMk3ProductDefs
from script.product_defs.launchkey88_product_defs import Launchkey88ProductDefs
from script.product_defs.launchkey_mk4_product_defs import LaunchkeyMk4ProductDefs
from script.product_defs.launchkey_product_defs import LaunchkeyProductDefs
from script.product_defs.launchkeymini_mk4_product_defs import LaunchkeyMiniMk4ProductDefs
from script.product_defs.launchkeymini_product_defs import LaunchkeyMiniProductDefs

__all__ = [
    "make_product_defs",
]


def make_product_defs(device_id):
    """Instantiates and returns the relevant implementation of ProductDefs.

    Args:
        device_id: Device for which to return an implementation of ProductDefs.

    Returns:
        Instance of a ProductDefs implementation.
    """
    if device_id == DeviceId.FLkey37 or device_id == DeviceId.FLkey49 or device_id == DeviceId.FLkey61:
        return FLkeyProductDefs()
    if device_id == DeviceId.FLkeyMini:
        return FLkeyMiniProductDefs()
    if device_id == DeviceId.LaunchkeyMini:
        return LaunchkeyMiniProductDefs()
    if device_id == DeviceId.Launchkey:
        return LaunchkeyProductDefs()
    if device_id == DeviceId.LaunchkeyMiniMk4:
        return LaunchkeyMiniMk4ProductDefs()
    if device_id == DeviceId.LaunchkeyMk4:
        return LaunchkeyMk4ProductDefs()
    if device_id == DeviceId.Launchkey88:
        return Launchkey88ProductDefs()
    if device_id == DeviceId.LaunchControlXlMk3:
        return LaunchControlXlMk3ProductDefs()
    return None
