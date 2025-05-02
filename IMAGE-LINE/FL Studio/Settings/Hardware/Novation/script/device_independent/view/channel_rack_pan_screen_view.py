from script.device_independent.util_view.view import View


class ChannelRackPanScreenView(View):
    def __init__(self, action_dispatcher, screen_writer, fl):
        super().__init__(action_dispatcher)
        self.screen_writer = screen_writer
        self.fl = fl

    def handle_ChannelPanChangedAction(self, action):
        self.display_pan(action.control, action.channel, action.value)

    def handle_ChannelPanPreviewedAction(self, action):
        if action.channel >= self.fl.channel_count():
            self.screen_writer.display_parameter(action.control, title="", name="Not Used", value="")
        else:
            self.display_pan(action.control, action.channel, action.value)

    def display_pan(self, control, channel, value):
        pan = value
        if abs(pan) < 1e-6:
            pan_str = "C"
        elif pan < 0:
            pan_str = f'{format(abs(pan) * 100, ".0f")}L'
        else:
            pan_str = f'{format(abs(pan) * 100, ".0f")}R'

        channel_name = self.fl.get_channel_name(channel)
        self.screen_writer.display_parameter(control, title=channel_name, name="Pan", value=pan_str)
