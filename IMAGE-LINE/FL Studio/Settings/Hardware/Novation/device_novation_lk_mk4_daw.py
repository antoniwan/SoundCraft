# name=Novation Launchkey MK4 DAW
# supportedHardwareIds=00 20 29 46 01 00 01,00 20 29 45 01 00 01,00 20 29 44 01 00 01,00 20 29 43 01 00 01
from script.constants import DeviceId
from script.device_adapters.fl_to_application_adapter import (
    add_fl_callbacks_to_namespace,
    make_fl_to_application_adapter,
)

device_id = DeviceId.LaunchkeyMk4
fl_to_application_adapter = make_fl_to_application_adapter(device_id)
add_fl_callbacks_to_namespace(globals(), fl_to_application_adapter)
