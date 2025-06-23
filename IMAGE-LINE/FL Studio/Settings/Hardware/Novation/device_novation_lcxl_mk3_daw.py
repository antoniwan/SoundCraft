# name=Novation Launch Control XL 3 DAW
# supportedHardwareIds=00 20 29 48 01 00 01,00 20 29 49 01 00 01,00 20 29 4A 01 00 01,00 20 29 4B 01 00 01,00 20 29 4C 01 00 01,00 20 29 4D 01 00 01,00 20 29 4E 01 00 01,00 20 29 4F 01 00 01
from script.constants import DeviceId
from script.device_adapters.fl_to_application_adapter import (
    add_fl_callbacks_to_namespace,
    make_fl_to_application_adapter,
)

device_id = DeviceId.LaunchControlXlMk3
fl_to_application_adapter = make_fl_to_application_adapter(device_id)
add_fl_callbacks_to_namespace(globals(), fl_to_application_adapter)
