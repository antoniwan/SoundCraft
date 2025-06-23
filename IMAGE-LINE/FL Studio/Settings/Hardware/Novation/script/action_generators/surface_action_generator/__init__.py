from script.constants import DeviceId

from .flkey_surface_action_generator import FLkeySurfaceActionGenerator
from .flkeymini_surface_action_generator import FLkeyMiniSurfaceActionGenerator
from .launchcontrolxl_mk3_surface_action_generator import LaunchControlXlMk3SurfaceActionGenerator
from .launchkey_mk4_surface_action_generator import LaunchkeyMk4SurfaceActionGenerator
from .launchkey_surface_action_generator import LaunchkeySurfaceActionGenerator
from .launchkeymini_mk4_surface_action_generator import LaunchkeyMiniMk4SurfaceActionGenerator
from .launchkeymini_surface_action_generator import LaunchkeyMiniSurfaceActionGenerator
from .surface_action_generator_wrapper import SurfaceActionGeneratorWrapper

__all__ = ["make_surface_action_generator"]


def make_surface_action_generator(device_id, action_dispatcher, product_defs):
    """Instantiates and returns the relevant implementation of SurfaceActionGenerator.

    Args:
        device_id: Device for which to return an implementation of SurfaceActionGenerator.
        action_dispatcher: required by SurfaceActionGenerator instance dispatch actions.

    Returns:
        Instance of a SurfaceActionGenerator implementation.
    """
    if device_id == DeviceId.FLkey37 or device_id == DeviceId.FLkey49 or device_id == DeviceId.FLkey61:
        return SurfaceActionGeneratorWrapper(action_dispatcher, FLkeySurfaceActionGenerator(product_defs))
    if device_id == DeviceId.FLkeyMini:
        return SurfaceActionGeneratorWrapper(action_dispatcher, FLkeyMiniSurfaceActionGenerator(product_defs))
    if device_id == DeviceId.LaunchkeyMini:
        return SurfaceActionGeneratorWrapper(action_dispatcher, LaunchkeyMiniSurfaceActionGenerator(product_defs))
    if device_id == DeviceId.Launchkey or device_id == DeviceId.Launchkey88:
        return SurfaceActionGeneratorWrapper(action_dispatcher, LaunchkeySurfaceActionGenerator(product_defs))
    if device_id == DeviceId.LaunchkeyMiniMk4:
        return SurfaceActionGeneratorWrapper(action_dispatcher, LaunchkeyMiniMk4SurfaceActionGenerator(product_defs))
    if device_id == DeviceId.LaunchkeyMk4:
        return SurfaceActionGeneratorWrapper(action_dispatcher, LaunchkeyMk4SurfaceActionGenerator(product_defs))
    if device_id == DeviceId.LaunchControlXlMk3:
        return SurfaceActionGeneratorWrapper(action_dispatcher, LaunchControlXlMk3SurfaceActionGenerator(product_defs))
    return None
