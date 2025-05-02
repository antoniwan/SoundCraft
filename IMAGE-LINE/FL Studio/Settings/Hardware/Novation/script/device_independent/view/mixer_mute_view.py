from script.actions import MixerMuteStateChangedAction
from script.colour_utils import clamp_brightness, scale_colour
from script.colours import Colours
from script.constants import LedLightingType, SoloMuteEditState
from script.device_independent.util_view import View
from script.device_independent.view.solo_mute_edit_state_machine import SoloMuteEditStateMachine


class MixerMuteView(View):
    button_functions = [
        "ToggleArmMute_1",
        "ToggleArmMute_2",
        "ToggleArmMute_3",
        "ToggleArmMute_4",
        "ToggleArmMute_5",
        "ToggleArmMute_6",
        "ToggleArmMute_7",
        "ToggleArmMute_8",
    ]

    def __init__(self, action_dispatcher, model, product_defs, fl, button_led_writer):
        super().__init__(action_dispatcher)
        self.model = model
        self.product_defs = product_defs
        self.fl = fl
        self.button_led_writer = button_led_writer
        self.state_machine = SoloMuteEditStateMachine(on_state_change=self._on_state_change)
        self.bright_colour_min_brightness = 100
        self.dim_colour_scale_factor = 0.25
        # self._on_state_change(self.state_machine.state)
        self.track_has_been_interacted_with_in_solo_mode = False

    def _on_show(self):
        self.update_leds()

    def _on_hide(self):
        self.turn_off_leds()

    def _on_state_change(self, previous_state):
        pass

    @property
    def button_to_track_index(self):
        tracks_in_bank = self.model.mixer_tracks_in_active_bank
        return {
            self.product_defs.FunctionToButton.get(function): track
            for function, track in zip(self.button_functions, tracks_in_bank)
        }

    def handle_ButtonPressedAction(self, action):
        if action.button in self.button_to_track_index:
            track_index = self.button_to_track_index[action.button]
            self.toggle_mute(track_index)
            self.state_machine.mute_button_pressed()

    def handle_MixerBankChangedAction(self, action):
        self.update_leds()

    def handle_AllMixerTracksChangedAction(self, action):
        self.update_leds()

    def get_colour_for_track(self, track_index):
        if self.fl.is_mixer_track_mute_enabled(track_index):
            return Colours.off
        if self.state_machine.state == SoloMuteEditState.Mute:
            return self.bright_track_colour(self.fl.get_mixer_track_colour(track_index))
        return self.dim_track_colour(self.fl.get_mixer_track_colour(track_index))

    def update_leds(self):
        self.turn_off_leds()
        arm_select_button = self.product_defs.FunctionToButton.get("ArmSelect")
        self.button_led_writer.set_button_colour(arm_select_button, Colours.mixer_track_mute)
        for button, track_index in self.button_to_track_index.items():
            colour = self.get_colour_for_track(track_index)
            self.button_led_writer.set_button_colour(button, colour, lighting_type=LedLightingType.RGB)

    def turn_off_leds(self):
        arm_select_button = self.product_defs.FunctionToButton.get("ArmSelect")
        self.button_led_writer.set_button_colour(arm_select_button, Colours.off)
        for function in self.button_functions:
            button = self.product_defs.FunctionToButton.get(function)
            self.button_led_writer.set_button_colour(button, Colours.off)

    def toggle_mute(self, track_index):
        enabled = not self.fl.is_mixer_track_mute_enabled(track_index)
        self.fl.toggle_mixer_track_mute(track_index)
        self.action_dispatcher.dispatch(MixerMuteStateChangedAction(track=track_index, enabled=enabled))

    def dim_track_colour(self, base_colour):
        return scale_colour(base_colour, self.dim_colour_scale_factor)

    def bright_track_colour(self, base_colour):
        return clamp_brightness(base_colour, minimum=self.bright_colour_min_brightness)
