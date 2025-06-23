from script.device_independent.util_view.view import View


class ChannelRackVolumeScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl

    def handle_ChannelVolumeChangedAction(self, action):
        self.display_volume(action.control, action.channel)

    def handle_ChannelVolumePreviewedAction(self, action):
        # The two calls to suspend_trigger in this method are another work-around for the FW bug CTRL-232.
        # When the FW bug is fixed, the suspend_trigger calls should be removed.
        self.screen_writer.suspend_trigger(True)
        if action.channel >= self.fl.channel_count():
            self.screen_writer.display_parameter(action.control, title="", name="Not Used", value="")
        else:
            self.display_volume(action.control, action.channel)
        self.screen_writer.suspend_trigger(False)

    def display_volume(self, control, channel):
        volume = self.fl.get_channel_volume_dB(channel)
        volume_str = "-Inf dB" if volume < -200 else f'{format(volume, ".1f")} dB'
        channel_name = self.fl.get_channel_name(channel)
        self.screen_writer.display_parameter(control, title=channel_name, name="Level", value=volume_str)
