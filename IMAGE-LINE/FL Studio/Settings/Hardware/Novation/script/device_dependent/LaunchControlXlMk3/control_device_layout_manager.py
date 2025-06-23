from script.action_generators.surface_action_generator.surface_actions import (
    ChannelMuteModeAction,
    ChannelSelectModeAction,
)
from script.colours import Colours
from script.constants import ChannelNavigationMode, Encoders, Faders
from script.device_independent.util_view import LedView
from script.device_independent.view import (
    ChannelBankNamesHighlightView,
    ChannelBankSelectedScreenView,
    ChannelBankView,
    ChannelMuteModeScreenView,
    ChannelMuteToggleView,
    ChannelRackPanPreviewView,
    ChannelRackPanScreenView,
    ChannelRackPanView,
    ChannelRackVolumePreviewView,
    ChannelRackVolumeScreenView,
    ChannelRackVolumeView,
    ChannelSelectedScreenView,
    ChannelSelectInBankView,
    ChannelSelectModeScreenView,
    ChannelSelectView,
    NotUsedPreviewView,
    PluginParameterLedView,
    PluginParameterPreviewView,
    PluginParameterScreenView,
    PluginParameterView,
)
from script.plugin import plugin_parameter_mappings
from util.control_to_index import make_control_to_index


class ControlDeviceLayoutManager:
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
        device_manager,
    ):
        self.action_dispatcher = action_dispatcher
        self.fl_window_manager = fl_window_manager
        self.command_dispatcher = command_dispatcher
        self.product_defs = product_defs
        self.device_manager = device_manager
        model.control_bank_navigation_mode = ChannelNavigationMode.Bank
        self.model = model
        encoders = {
            **{
                index: product_defs.EncoderIndexToControlIndex.get(encoder)
                for index, encoder in enumerate(range(product_defs.Constants.NumEncoders.value))
            },
        }
        encoder_row1_to_index = make_control_to_index(
            product_defs.Constants.EncoderRow1FirstIndex.value, Encoders.Num.value
        )
        encoder_row3_to_index = make_control_to_index(
            product_defs.Constants.EncoderRow3FirstIndex.value, Encoders.Num.value
        )
        fader_to_index = make_control_to_index(Faders.FirstControlIndex.value, Faders.NumRegularFaders.value)
        self.channel_bank_names_highlight_view = ChannelBankNamesHighlightView(
            action_dispatcher,
            fl,
            model,
            num_channels=product_defs.Constants.ChannelsPerBank.value,
        )
        self.channel_bank_view = ChannelBankView(
            action_dispatcher,
            button_led_writer,
            fl,
            product_defs,
            model,
            decrement_button="SelectPreviousChannelBank",
            increment_button="SelectNextChannelBank",
        )
        self.channel_bank_selected_screen_view = ChannelBankSelectedScreenView(
            action_dispatcher, screen_writer, fl, model
        )
        self.channel_select_view = ChannelSelectView(action_dispatcher, button_led_writer, fl, product_defs)
        self.channel_selected_screen_view = ChannelSelectedScreenView(action_dispatcher, screen_writer, fl)
        self.channel_rack_pan_view = ChannelRackPanView(
            action_dispatcher, fl, model, product_defs, button_led_writer, control_to_index=encoder_row3_to_index
        )
        self.channel_rack_pan_screen_view = ChannelRackPanScreenView(action_dispatcher, screen_writer, fl)
        self.channel_rack_pan_preview_view = ChannelRackPanPreviewView(
            action_dispatcher, fl, product_defs, model, control_to_index=encoder_row3_to_index
        )
        self.channel_rack_volume_view = ChannelRackVolumeView(
            action_dispatcher, fl, model, control_to_index=fader_to_index
        )
        self.channel_rack_volume_screen_view = ChannelRackVolumeScreenView(action_dispatcher, screen_writer, fl)
        self.channel_rack_volume_preview_view = ChannelRackVolumePreviewView(
            action_dispatcher, product_defs, model, control_to_index=fader_to_index
        )
        self.channel_mute_toggle_view = ChannelMuteToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.channel_select_in_bank_view = ChannelSelectInBankView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.channel_mute_mode_screen_view = ChannelMuteModeScreenView(action_dispatcher, screen_writer)
        self.channel_select_mode_screen_view = ChannelSelectModeScreenView(action_dispatcher, screen_writer)
        self.plugin_parameter_view = PluginParameterView(
            action_dispatcher, fl, plugin_parameter_mappings, control_to_index=encoder_row1_to_index
        )
        self.plugin_parameter_led_view = PluginParameterLedView(
            action_dispatcher,
            button_led_writer,
            fl,
            product_defs,
            plugin_parameter_mappings,
            control_to_index=encoder_row1_to_index,
        )
        self.plugin_parameter_screen_view = PluginParameterScreenView(
            action_dispatcher, fl, screen_writer, plugin_parameter_mappings, control_to_index=encoder_row1_to_index
        )
        self.plugin_parameter_preview_view = PluginParameterPreviewView(
            action_dispatcher,
            fl,
            product_defs,
            plugin_parameter_mappings,
            control_to_index=encoder_row1_to_index,
        )
        self.not_used_led_views = []
        self.not_used_preview_views = []
        for index in range(
            product_defs.Constants.EncoderRow2FirstIndex.value, product_defs.Constants.EncoderRow3FirstIndex.value
        ):
            self.not_used_preview_views.append(
                NotUsedPreviewView(action_dispatcher, product_defs, screen_writer, control_index=encoders[index])
            )
            self.not_used_led_views.append(
                LedView(
                    action_dispatcher,
                    product_defs,
                    button_led_writer,
                    cc=encoders[index] + product_defs.Constants.EncoderCcOffset.value,
                    colour=Colours.off,
                )
            )

    @property
    def views(self):
        return [
            self.channel_bank_names_highlight_view,
            (self.channel_select_view if self.is_control_bank_navigation_mode_single else self.channel_bank_view),
            self.channel_selected_screen_view,
            self.channel_bank_selected_screen_view,
            self.channel_rack_pan_view,
            self.channel_rack_pan_screen_view,
            self.channel_rack_pan_preview_view,
            self.channel_rack_volume_view,
            self.channel_rack_volume_screen_view,
            self.channel_rack_volume_preview_view,
            self.channel_mute_toggle_view,
            self.channel_select_in_bank_view,
            self.channel_mute_mode_screen_view,
            self.channel_select_mode_screen_view,
            self.plugin_parameter_view,
            self.plugin_parameter_led_view,
            self.plugin_parameter_screen_view,
            self.plugin_parameter_preview_view,
            *self.not_used_led_views,
            *self.not_used_preview_views,
        ]

    @property
    def is_control_bank_navigation_mode_single(self):
        return self.model.control_bank_navigation_mode != ChannelNavigationMode.Bank

    def show(self):
        self.device_manager.enable_encoder_mode()
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
        self.fl_window_manager.focus_channel_window()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ShiftModifier"):
            self._set_control_bank_navigation_mode(ChannelNavigationMode.Single)
        if action.button == self.product_defs.FunctionToButton.get("SoloArm"):
            self._show_channel_select_mode()
        elif action.button == self.product_defs.FunctionToButton.get("MuteSelect"):
            self._show_channel_mute_mode()

    def handle_ButtonReleasedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("ShiftModifier"):
            self._set_control_bank_navigation_mode(ChannelNavigationMode.Bank)

    def _set_control_bank_navigation_mode(self, control_bank_navigation_mode):
        if self.model.control_bank_navigation_mode != control_bank_navigation_mode:
            self.hide()
            self.model.control_bank_navigation_mode = control_bank_navigation_mode
            self.show()
            self.focus_windows()

    def _show_channel_select_mode(self):
        self.action_dispatcher.dispatch(ChannelSelectModeAction())

    def _show_channel_mute_mode(self):
        self.action_dispatcher.dispatch(ChannelMuteModeAction())
