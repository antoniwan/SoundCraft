from script.action_generators.surface_action_generator.surface_actions import ArmSelectStateChangedAction
from script.constants import ChannelNavigationMode, FaderArmMuteMode, Faders
from script.device_independent.view import (
    MixerArmMuteScreenView,
    MixerMuteView,
    MixerTrackRecordArmToggleView,
    MixerVolumeView,
)
from util.control_to_index import make_control_to_index


class VolumeFaderLayoutManager:
    def __init__(
        self,
        action_dispatcher,
        command_dispatcher,
        fl,
        model,
        fl_window_manager,
        product_defs,
        button_led_writer,
        screen_writer,
    ):
        self.action_dispatcher = action_dispatcher
        self.fl_window_manager = fl_window_manager
        self.command_dispatcher = command_dispatcher
        self.product_defs = product_defs
        self.model = model
        self.button_led_writer = button_led_writer
        control_to_index = make_control_to_index(Faders.FirstControlIndex.value, Faders.NumRegularFaders.value)
        self.fader_view = MixerVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index)
        self.arm_mute_screen_view = MixerArmMuteScreenView(action_dispatcher, screen_writer)
        self.mixer_record_arm_view = MixerTrackRecordArmToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_mute_view = MixerMuteView(action_dispatcher, model, product_defs, fl, button_led_writer)

    @property
    def views(self):
        return {
            self.fader_view,
            self.arm_mute_screen_view,
            self.mixer_record_arm_view if self.is_mixer_record_arm_view_enabled else self.mixer_mute_view,
        }

    @property
    def is_mixer_record_arm_view_enabled(self):
        return self.model.mixer_arm_mute_mode is not FaderArmMuteMode.Mute

    def show(self):
        self.action_dispatcher.subscribe(self)
        self.model.channel_rack.navigation_mode = ChannelNavigationMode.Bank
        for view in self.views:
            view.show()

    def hide(self):
        self.action_dispatcher.unsubscribe(self)
        for view in self.views:
            view.hide()

    def focus_windows(self):
        self.fl_window_manager.hide_last_focused_plugin_window()
        self.fl_window_manager.focus_mixer_window()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ArmSelect"):
            self._toggle_arm_select_views()

    def _toggle_arm_select_views(self):
        self.hide()
        mode = FaderArmMuteMode.Mute if self.is_mixer_record_arm_view_enabled else FaderArmMuteMode.Arm
        self.model.mixer_arm_mute_mode = mode
        self.show()
        self.focus_windows()
        self.action_dispatcher.dispatch(ArmSelectStateChangedAction(mode=mode))
