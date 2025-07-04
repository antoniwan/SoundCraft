from script.action_generators.surface_action_generator.surface_actions import DeviceLayoutChangedAction


class KeyboardControllerCommonDeviceLayoutActionGenerator:
    def __init__(self, product_defs):
        self.product_defs = product_defs

    def handle_midi_event(self, fl_event):
        event_type = fl_event.status, fl_event.data1
        if event_type == self.product_defs.SurfaceEvent.DeviceLayout.value:
            return [DeviceLayoutChangedAction(layout=fl_event.data2)]
        return []
