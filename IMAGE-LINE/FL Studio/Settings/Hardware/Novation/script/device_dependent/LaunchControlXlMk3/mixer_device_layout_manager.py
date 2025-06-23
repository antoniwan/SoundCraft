from script.action_generators.surface_action_generator.surface_actions import (
    MuteSelectStateChangedAction,
    SoloArmStateChangedAction,
)
from script.colours import Colours
from script.constants import ChannelNavigationMode, Encoders, FaderMuteSelectMode, Faders, FaderSoloArmMode
from script.device_independent.util_view import LedView
from script.device_independent.view import (
    MixerBankButtonView,
    MixerBankHighlightView,
    MixerBankScreenView,
    MixerMuteSelectScreenView,
    MixerPanPreviewView,
    MixerPanScreenView,
    MixerPanView,
    MixerSoloArmScreenView,
    MixerTrackEqPreviewView,
    MixerTrackEqScreenView,
    MixerTrackEqView,
    MixerTrackMuteToggleView,
    MixerTrackRecordArmToggleView,
    MixerTrackSelectedScreenView,
    MixerTrackSelectInBankView,
    MixerTrackSelectView,
    MixerTrackSoloToggleView,
    MixerVolumeScreenView,
    MixerVolumeView,
    NotUsedPreviewView,
    TransportMarkerPreviewView,
    TransportMarkerScreenView,
    TransportMarkerView,
    TransportSongPositionPreviewView,
    TransportSongPositionScreenView,
    TransportSongPositionView,
    TransportTempoPreviewView,
    TransportTempoScreenView,
    TransportTempoView,
    TransportZoomPreviewView,
    TransportZoomScreenView,
    TransportZoomView,
)
from util.control_to_index import make_control_to_index


class MixerDeviceLayoutManager:
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
        model.mixer_solo_arm_mode = FaderSoloArmMode.Arm
        model.mixer_mute_select_mode = FaderMuteSelectMode.Mute
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
        self.mixer_bank_view = MixerBankButtonView(action_dispatcher, button_led_writer, fl, product_defs, model)
        self.mixer_bank_highlight_view = MixerBankHighlightView(action_dispatcher, fl, model)
        self.mixer_bank_screen_view = MixerBankScreenView(action_dispatcher, screen_writer, model)
        self.mixer_track_select_view = MixerTrackSelectView(
            action_dispatcher, product_defs, model, button_led_writer, fl
        )
        self.mixer_volume_view = MixerVolumeView(action_dispatcher, fl, model, control_to_index=fader_to_index)
        self.mixer_volume_screen_view = MixerVolumeScreenView(action_dispatcher, screen_writer, fl)
        self.mixer_mute_select_screen_view = MixerMuteSelectScreenView(action_dispatcher, screen_writer)
        self.mixer_solo_arm_screen_view = MixerSoloArmScreenView(action_dispatcher, screen_writer)
        self.mixer_track_solo_toggle_view = MixerTrackSoloToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_track_record_arm_toggle_view = MixerTrackRecordArmToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_track_mute_toggle_view = MixerTrackMuteToggleView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_track_select_in_bank_view = MixerTrackSelectInBankView(
            action_dispatcher, product_defs, fl, model, button_led_writer
        )
        self.mixer_track_selected_screen_view = MixerTrackSelectedScreenView(
            action_dispatcher, screen_writer, fl, show_index_in_primary_text=True
        )
        self.mixer_pan_view = MixerPanView(
            action_dispatcher, fl, model, product_defs, button_led_writer, control_to_index=encoder_row3_to_index
        )
        self.mixer_pan_screen_view = MixerPanScreenView(action_dispatcher, screen_writer, fl)
        self.mixer_pan_preview_view = MixerPanPreviewView(
            action_dispatcher, fl, product_defs, model, control_to_index=encoder_row3_to_index
        )
        self.mixer_track_eq_view = MixerTrackEqView(
            action_dispatcher, fl, product_defs, button_led_writer, control_to_index=encoder_row1_to_index
        )
        self.mixer_track_eq_screen_view = MixerTrackEqScreenView(action_dispatcher, screen_writer, fl)
        self.mixer_track_eq_preview_view = MixerTrackEqPreviewView(action_dispatcher)
        self.transport_song_position_view = TransportSongPositionView(action_dispatcher, fl, control_index=encoders[8])
        self.transport_song_position_screen_view = TransportSongPositionScreenView(
            action_dispatcher, fl, screen_writer, control_index=encoders[8]
        )
        self.transport_song_position_preview_view = TransportSongPositionPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[8]
        )
        self.transport_song_position_led_view = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[8] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.transport_song_position,
        )
        self.transport_zoom_view = TransportZoomView(action_dispatcher, fl, control_index=encoders[9])
        self.transport_zoom_screen_view = TransportZoomScreenView(
            action_dispatcher, screen_writer, control_index=encoders[9]
        )
        self.transport_zoom_preview_view = TransportZoomPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[9]
        )
        self.transport_zoom_led_view = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[9] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.transport_zoom,
        )
        self.transport_marker_view = TransportMarkerView(action_dispatcher, fl, control_index=encoders[12])
        self.transport_marker_screen_view = TransportMarkerScreenView(
            action_dispatcher, screen_writer, control_index=encoders[12]
        )
        self.transport_marker_preview_view = TransportMarkerPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[12]
        )
        self.transport_marker_led_view = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[12] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.transport_marker,
        )
        self.transport_tempo_view = TransportTempoView(action_dispatcher, fl, control_index=encoders[15])
        self.transport_tempo_screen_view = TransportTempoScreenView(
            action_dispatcher, fl, screen_writer, control_index=encoders[15]
        )
        self.transport_tempo_preview_view = TransportTempoPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[15]
        )
        self.transport_tempo_led_view = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[15] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.transport_tempo,
        )
        self.transport_not_used_preview_view_2 = NotUsedPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[10]
        )
        self.transport_not_used_led_view_2 = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[10] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.off,
        )
        self.transport_not_used_preview_view_3 = NotUsedPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[11]
        )
        self.transport_not_used_led_view_3 = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[11] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.off,
        )
        self.transport_not_used_preview_view_5 = NotUsedPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[13]
        )
        self.transport_not_used_led_view_5 = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[13] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.off,
        )
        self.transport_not_used_preview_view_6 = NotUsedPreviewView(
            action_dispatcher, product_defs, screen_writer, control_index=encoders[14]
        )
        self.transport_not_used_led_view_6 = LedView(
            action_dispatcher,
            product_defs,
            button_led_writer,
            cc=encoders[14] + product_defs.Constants.EncoderCcOffset.value,
            colour=Colours.off,
        )

    @property
    def views(self):
        return [
            self.mixer_bank_highlight_view,
            self.mixer_bank_view,
            self.mixer_bank_screen_view,
            self.mixer_mute_select_screen_view,
            self.mixer_solo_arm_screen_view,
            self.mixer_track_select_view,
            self.mixer_track_selected_screen_view,
            self.mixer_volume_view,
            self.mixer_volume_screen_view,
            (
                self.mixer_track_record_arm_toggle_view
                if self.is_mixer_record_arm_view_enabled
                else self.mixer_track_solo_toggle_view
            ),
            (
                self.mixer_track_mute_toggle_view
                if self.is_mixer_track_mute_view_enabled
                else self.mixer_track_select_in_bank_view
            ),
            self.mixer_pan_view,
            self.mixer_pan_screen_view,
            self.mixer_pan_preview_view,
            self.mixer_track_eq_view,
            self.mixer_track_eq_screen_view,
            self.mixer_track_eq_preview_view,
            self.transport_song_position_view,
            self.transport_song_position_screen_view,
            self.transport_song_position_preview_view,
            self.transport_song_position_led_view,
            self.transport_zoom_view,
            self.transport_zoom_screen_view,
            self.transport_zoom_preview_view,
            self.transport_zoom_led_view,
            self.transport_marker_view,
            self.transport_marker_screen_view,
            self.transport_marker_preview_view,
            self.transport_marker_led_view,
            self.transport_tempo_view,
            self.transport_tempo_screen_view,
            self.transport_tempo_preview_view,
            self.transport_tempo_led_view,
            self.transport_not_used_preview_view_2,
            self.transport_not_used_led_view_2,
            self.transport_not_used_preview_view_3,
            self.transport_not_used_led_view_3,
            self.transport_not_used_preview_view_5,
            self.transport_not_used_led_view_5,
            self.transport_not_used_preview_view_6,
            self.transport_not_used_led_view_6,
        ]

    @property
    def is_mixer_record_arm_view_enabled(self):
        return self.model.mixer_solo_arm_mode is not FaderSoloArmMode.Solo

    @property
    def is_mixer_track_mute_view_enabled(self):
        return self.model.mixer_mute_select_mode is not FaderMuteSelectMode.Select

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
        self.fl_window_manager.focus_mixer_window()

    def handle_ButtonPressedAction(self, action):
        if action.button == self.product_defs.FunctionToButton.get("SoloArm"):
            self._toggle_solo_arm_views()
        elif action.button == self.product_defs.FunctionToButton.get("MuteSelect"):
            self._toggle_mute_select_views()
        elif action.button == self.product_defs.FunctionToButton.get("ShiftModifier"):
            self.focus_windows()

    def _toggle_solo_arm_views(self):
        self.hide()
        mode = FaderSoloArmMode.Solo if self.is_mixer_record_arm_view_enabled else FaderSoloArmMode.Arm
        self.model.mixer_solo_arm_mode = mode
        self.show()
        self.focus_windows()
        self.action_dispatcher.dispatch(SoloArmStateChangedAction(mode=mode))

    def _toggle_mute_select_views(self):
        self.hide()
        mode = FaderMuteSelectMode.Select if self.is_mixer_track_mute_view_enabled else FaderMuteSelectMode.Mute
        self.model.mixer_mute_select_mode = mode
        self.show()
        self.focus_windows()
        self.action_dispatcher.dispatch(MuteSelectStateChangedAction(mode=mode))
