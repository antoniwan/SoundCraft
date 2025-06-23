import time

from script.constants import DisplayPriority, SysEx
from util.custom_enum import CustomEnum


class LaunchkeyMk4RangeScreenWriter:
    def __init__(self, sender, product_defs):
        self.sender = sender
        self.product_defs = product_defs
        sysex_message_header = SysEx.MessageHeader.value + [product_defs.Constants.NovationProductId.value]
        self._configure_display_header = sysex_message_header + [self.DisplaySysexCommand.ConfigureDisplay.value]
        self._display_text_header = sysex_message_header + [self.DisplaySysexCommand.DisplayText.value]
        self._config_cache = {}
        self._display_cache = {}
        self._last_trigger_time = 0
        self._trigger_limit_period = self.TriggerLimitPeriod.Permanent.value
        self._suspend_trigger = False

    class DisplayConfig(CustomEnum):
        TwoLines = 0x01
        ThreeLines = 0x02
        Grid = 0x03
        TouchEnabled = 0x20
        AutoTrigger = 0x40

    class DisplayField(CustomEnum):
        F0 = 0x00
        F1 = 0x01
        F2 = 0x02
        Trigger = 0x40

    class DisplaySysexCommand(CustomEnum):
        ConfigureDisplay = 0x04
        DisplayText = 0x06

    class TriggerLimitPeriod(CustomEnum):
        Permanent = 0.5
        Overlay = 0.1

    def _configure_display_target(self, target, config):
        cached_config = self._config_cache.get(target)
        if cached_config != config:
            self._config_cache[target] = config
            configure_display_message = self._configure_display_header + [target, config]
            self.sender.send_sysex(configure_display_message)

    def _control_index_to_address(self, control_index):
        address = self.product_defs.ControlIndexToEncoderIndex.get(control_index)
        if address is not None:
            address += self.product_defs.DisplayAddress.FirstEncoder.value
        else:
            address = self.product_defs.ControlIndexToFaderIndex.get(control_index)
            if address is not None:
                address += self.product_defs.DisplayAddress.FirstFader.value
        return address

    def _display_text(self, address, field, trigger, text):
        if trigger and (
            address < self.product_defs.DisplayAddress.FirstEncoder
            or address > self.product_defs.DisplayAddress.LastEncoder
        ):
            field = self._update_last_trigger(address, field)

        text = text if text is not None else ""

        display_text_message = (
            self._display_text_header + [address, field] + list(text.encode(encoding="ascii", errors="replace"))
        )
        self.sender.send_sysex(display_text_message)

    def _is_fader_address(self, address):
        return (
            address >= self.product_defs.DisplayAddress.FirstFader
            and address <= self.product_defs.DisplayAddress.LastFader
        )

    def _is_encoder_address(self, address):
        return (
            address >= self.product_defs.DisplayAddress.FirstEncoder
            and address <= self.product_defs.DisplayAddress.LastEncoder
        )

    def _update_display(self, address, topLine, middleLine, bottomLine=None):
        args = (topLine, middleLine, bottomLine)
        cached_args = self._display_cache.get(address)
        if args != cached_args:
            self._display_cache[address] = args

            config = (
                self.DisplayConfig.ThreeLines.value if bottomLine is not None else self.DisplayConfig.TwoLines.value
            )

            if self._is_encoder_address(address) and topLine is not None and middleLine is not None:
                config |= self.DisplayConfig.TouchEnabled.value | self.DisplayConfig.AutoTrigger.value

            self._configure_display_target(address, config)

            if bottomLine is not None:
                self._display_text(address, self.DisplayField.F2.value, False, bottomLine)
            self._display_text(address, self.DisplayField.F1.value, False, middleLine)
            self._display_text(address, self.DisplayField.F0.value, True, topLine)

    def _update_display_grid(self, address, topLine, fields):
        args = topLine, *fields
        cached_args = self._display_cache.get(address)
        if args != cached_args:
            self._display_cache[address] = args
            self._configure_display_target(address, self.DisplayConfig.Grid.value)
            for i in range(8):
                self._display_text(
                    address, i + 1, False, fields[i] if i < len(fields) and fields[i] is not None else "-"
                )
            self._display_text(address, 0, True, topLine)

    def _update_last_trigger(self, address, field):
        if not self._suspend_trigger:
            now = time.time()
            if address == self.product_defs.DisplayAddress.Permanent.value:
                field |= self.DisplayField.Trigger.value
                self._last_trigger_time = now
                self._trigger_limit_period = self.TriggerLimitPeriod.Permanent.value
            elif address == self.product_defs.DisplayAddress.Overlay.value:
                if self._last_trigger_time > 0 and now - self._last_trigger_time > self._trigger_limit_period:
                    field |= self.DisplayField.Trigger.value
                    self._last_trigger_time = now
                    self._trigger_limit_period = self.TriggerLimitPeriod.Overlay.value
            elif not self._is_encoder_address(address):
                # The above check should also include `not _is_fader_address`. That has been removed to work around a FW bug where incorrect values are displayed when faders are moved quickly.
                # Related tickets: FCT-686, FCT-674, CTRL-292
                # Once the FW bug is fixed, this `not is_fader_address` should be added back in.
                if now - self._last_trigger_time > self._trigger_limit_period:
                    field |= self.DisplayField.Trigger.value
        return field

    def display_notification(self, primary_text="", secondary_text=""):
        self._update_display(self.product_defs.DisplayAddress.Overlay.value, primary_text, secondary_text)

    def display_parameter(self, control_index, *, title, name, value, priority=DisplayPriority.Title):
        address = self._control_index_to_address(control_index)
        if address is not None:
            if title is None:
                self._update_display(address, name, value)
            else:
                self._update_display(address, title, name, value)

    def display_idle(self, text, fields=None):
        if fields is None:
            # Do not allow empty text to be displayed on the permanent display, its not allowed on LK4.
            if not text:
                text = "FL Studio"
            self._update_display(self.product_defs.DisplayAddress.Permanent.value, "", text, "")
        else:
            self._update_display_grid(self.product_defs.DisplayAddress.Permanent.value, text, fields)

    def reset(self):
        self._config_cache.clear()
        self._display_cache.clear()

    # This method is used to suspend the manual-trigger bits being set in the screen sysex messages.
    # Currently its only used as a work-around to prevent manually triggered fader displays.
    # This work-around is required because of another work-around for a FW bug that causes incorrect display values when faders are moved quickly.
    # Related tickets: FCT-686, FCT-674, CTRL-292
    # Once the FW bug is fixed, this method (and calls to it) should be removed.
    def suspend_trigger(self, suspend):
        self._suspend_trigger = suspend
