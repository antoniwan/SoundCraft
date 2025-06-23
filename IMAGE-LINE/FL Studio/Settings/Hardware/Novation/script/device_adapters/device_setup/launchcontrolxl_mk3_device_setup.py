class LaunchControlXlMk3DeviceSetup:
    def __init__(self, sender, product_defs):
        self.sender = sender
        self.product_defs = product_defs

    def init(self):
        self._enter_daw_mode()
        self._select_device_layout_mixer()

    def deinit(self):
        self._exit_daw_mode()

    def _enter_daw_mode(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.EnterDawMode.value)

    def _exit_daw_mode(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.ExitDawMode.value)

    def _select_device_layout_mixer(self):
        self.sender.send_message(
            *self.product_defs.SurfaceEvent.DeviceLayout.value, self.product_defs.DeviceLayout.Mixer.value
        )
