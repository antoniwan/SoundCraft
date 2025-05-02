class LaunchkeyMiniMk4DeviceSetup:
    def __init__(self, sender, product_defs):
        self.sender = sender
        self.product_defs = product_defs

    def init(self):
        self._enter_daw_mode()
        self._take_ownership_of_drumrack()
        self._select_encoder_layout_plugin()
        self._select_pad_layout_channel_rack()

    def deinit(self):
        self._release_ownership_of_drumrack()
        self._exit_daw_mode()

    def _enter_daw_mode(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.EnterDawMode.value)

    def _exit_daw_mode(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.ExitDawMode.value)

    def _select_encoder_layout_plugin(self):
        self.sender.send_message(
            *self.product_defs.SurfaceEvent.EncoderLayout.value, self.product_defs.EncoderLayout.Plugin.value
        )

    def _select_pad_layout_channel_rack(self):
        self.sender.send_message(
            *self.product_defs.SurfaceEvent.PadLayout.value, self.product_defs.PadLayout.ChannelRack.value
        )

    def _take_ownership_of_drumrack(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.TakeOwnershipOfDrumrack.value)

    def _release_ownership_of_drumrack(self):
        self.sender.send_message(*self.product_defs.SurfaceEvent.ReleaseOwnershipOfDrumrack.value)
