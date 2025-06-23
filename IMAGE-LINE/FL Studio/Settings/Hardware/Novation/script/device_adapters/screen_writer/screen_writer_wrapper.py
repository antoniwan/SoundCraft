from script.constants import DisplayPriority


class ScreenWriterWrapper:
    def __init__(self, screen_writer):
        self.screen_writer = screen_writer
        self.most_recently_used_display_parameter_args = None
        self.most_recently_used_display_parameter_name_args = None
        self.most_recently_used_display_parameter_value_args = None

    def reset(self):
        self.most_recently_used_display_parameter_name_args = None
        self.most_recently_used_display_parameter_value_args = None

    def display_parameter(self, control_index, *, title, name, value, priority=DisplayPriority.Title):
        if self.screen_writer:
            args = (control_index, title, name, value)
            if args != self.most_recently_used_display_parameter_args:
                self.most_recently_used_display_parameter_args = args
                self.screen_writer.display_parameter_name(
                    control_index, name if priority == DisplayPriority.Name else title
                )
                self.screen_writer.display_parameter_value(control_index, value)

    def display_parameter_name(self, control_index, name):
        if self.screen_writer:
            args = (control_index, name)
            if args != self.most_recently_used_display_parameter_name_args:
                self.most_recently_used_display_parameter_name_args = args
                self.screen_writer.display_parameter_name(*args)

    def display_parameter_value(self, control_index, value):
        if self.screen_writer:
            args = (control_index, value)
            if args != self.most_recently_used_display_parameter_value_args:
                self.most_recently_used_display_parameter_value_args = args
                self.screen_writer.display_parameter_value(*args)

    def display_notification(self, primary_text="", secondary_text=""):
        if self.screen_writer:
            self.screen_writer.display_notification(primary_text, secondary_text)

    def display_idle(self, text, fields=None):
        pass

    # This method is used to suspend the manual-trigger bits being set in the screen sysex messages.
    # Currently its only used as a work-around to prevent manually triggered fader displays.
    # This work-around is required because of another work-around for a FW bug that causes incorrect display values when faders are moved quickly.
    # Related tickets: FCT-686, FCT-674, CTRL-292
    # Once the FW bug is fixed, this method (and calls to it) should be removed.
    def suspend_trigger(self, suspend):
        pass
