from script.constants import ChannelNavigationMode, Encoders, MixerEncoderMode
from script.device_dependent.LaunchkeyMk4Range.paged_layout_manager import PagedLayoutManager
from script.device_independent.view import (
    ChannelRackPanPreviewView,
    ChannelRackPanScreenView,
    ChannelRackPanView,
    ChannelRackVolumePreviewView,
    ChannelRackVolumeScreenView,
    ChannelRackVolumeView,
    FLStudioTextView,
    MixerPanPreviewView,
    MixerPanScreenView,
    MixerPanView,
    MixerTrackEqPreviewView,
    MixerTrackEqScreenView,
    MixerTrackEqView,
    MixerVolumePreviewView,
    MixerVolumeScreenView,
    MixerVolumeView,
)
from util.control_to_index import make_control_to_index


class MixerEncoderLayoutManager(PagedLayoutManager):
    def __init__(
        self,
        action_dispatcher,
        fl,
        product_defs,
        model,
        fl_window_manager,
        screen_writer,
        button_led_writer,
        device_manager,
    ):
        self.fl_window_manager = fl_window_manager
        self.device_manager = device_manager
        self.model = model
        control_to_index = make_control_to_index(Encoders.FirstControlIndex.value, Encoders.Num.value)
        layouts = [
            PagedLayoutManager.Layout(
                layout_id=MixerEncoderMode.ChannelRackVolume.value,
                notification_primary="Mixer",
                notification_secondary="Channel Volume",
                views=[
                    FLStudioTextView(screen_writer, action_dispatcher),
                    ChannelRackVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index),
                    ChannelRackVolumeScreenView(action_dispatcher, screen_writer, fl),
                    ChannelRackVolumePreviewView(
                        action_dispatcher, product_defs, model, control_to_index=control_to_index
                    ),
                ],
            ),
            PagedLayoutManager.Layout(
                layout_id=MixerEncoderMode.ChannelRackPan.value,
                notification_primary="Mixer",
                notification_secondary="Channel Pan",
                views=[
                    FLStudioTextView(screen_writer, action_dispatcher),
                    ChannelRackPanView(action_dispatcher, fl, model, control_to_index=control_to_index),
                    ChannelRackPanScreenView(action_dispatcher, screen_writer, fl),
                    ChannelRackPanPreviewView(
                        action_dispatcher, fl, product_defs, model, control_to_index=control_to_index
                    ),
                ],
            ),
            PagedLayoutManager.Layout(
                layout_id=MixerEncoderMode.MixerVolume.value,
                notification_primary="Mixer",
                notification_secondary="Mixer Volume",
                views=[
                    FLStudioTextView(screen_writer, action_dispatcher),
                    MixerVolumeView(action_dispatcher, fl, model, control_to_index=control_to_index),
                    MixerVolumeScreenView(action_dispatcher, screen_writer, fl),
                    MixerVolumePreviewView(action_dispatcher, product_defs, model),
                ],
            ),
            PagedLayoutManager.Layout(
                layout_id=MixerEncoderMode.MixerPan.value,
                notification_primary="Mixer",
                notification_secondary="Mixer Pan",
                views=[
                    FLStudioTextView(screen_writer, action_dispatcher),
                    MixerPanView(action_dispatcher, fl, model, control_to_index=control_to_index),
                    MixerPanScreenView(action_dispatcher, screen_writer, fl),
                    MixerPanPreviewView(action_dispatcher, fl, product_defs, model, control_to_index=control_to_index),
                ],
            ),
            PagedLayoutManager.Layout(
                layout_id=MixerEncoderMode.MixerEQ,
                notification_primary="Mixer",
                notification_secondary="Mixer EQ",
                views=[
                    FLStudioTextView(screen_writer, action_dispatcher),
                    MixerTrackEqView(action_dispatcher, fl, control_to_index=control_to_index),
                    MixerTrackEqScreenView(action_dispatcher, screen_writer, fl),
                    MixerTrackEqPreviewView(action_dispatcher),
                ],
            ),
        ]
        super().__init__(
            action_dispatcher,
            product_defs,
            screen_writer,
            button_led_writer,
            layouts,
            "SelectNextMixerEncoderMode",
            "SelectPreviousMixerEncoderMode",
        )

    @property
    def is_controlling_channel_rack(self):
        return (
            self.active_layout == MixerEncoderMode.ChannelRackVolume.value
            or self.active_layout == MixerEncoderMode.ChannelRackPan.value
        )

    def show(self):
        if self.model.mixer_encoder_mode is not None:
            self.set_layout(self.model.mixer_encoder_mode)

        super().show()
        self.device_manager.enable_encoder_mode()

    def focus_windows(self):
        self.fl_window_manager.hide_last_focused_plugin_window()
        if self.is_controlling_channel_rack:
            self.fl_window_manager.focus_channel_window()
        else:
            self.fl_window_manager.focus_mixer_window()

    def on_layout_selected(self, layout_id):
        self.model.mixer_encoder_mode = layout_id
        if self.is_controlling_channel_rack:
            self.model.channel_rack.navigation_mode = ChannelNavigationMode.Bank
        self.focus_windows()
