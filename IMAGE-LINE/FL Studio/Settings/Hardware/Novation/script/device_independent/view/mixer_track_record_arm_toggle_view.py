from script.colours import Colours
from script.constants import LedLightingType
from script.device_independent.util_view import View
from script.fl_constants import RefreshFlags


class MixerTrackRecordArmToggleView(View):
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

    def __init__(self, action_dispatcher, product_defs, fl, model, button_led_writer):
        super().__init__(action_dispatcher)
        self.action_dispatcher = action_dispatcher
        self.product_defs = product_defs
        self.button_led_writer = button_led_writer
        self.fl = fl
        self.model = model

    def _on_show(self):
        self.update_leds()

    def _on_hide(self):
        self.turn_off_leds()

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
            self.fl.toggle_mixer_track_arm(track_index)

    def handle_MixerBankChangedAction(self, action):
        self.update_leds()

    def handle_OnRefreshAction(self, action):
        if action.flags & RefreshFlags.LedUpdate.value:
            self.update_leds()

    def get_colour_for_track(self, track_index):
        if self.fl.is_mixer_track_armed(track_index):
            return Colours.mixer_track_record_arm_on
        return Colours.mixer_track_record_arm_off

    def update_leds(self):
        self.turn_off_leds()
        arm_select_button = self.product_defs.FunctionToButton.get("ArmSelect")
        self.button_led_writer.set_button_colour(arm_select_button, Colours.mixer_track_record_arm_on)
        for button, track_index in self.button_to_track_index.items():
            colour = self.get_colour_for_track(track_index)
            self.button_led_writer.set_button_colour(button, colour, lighting_type=LedLightingType.RGB)

    def turn_off_leds(self):
        arm_select_button = self.product_defs.FunctionToButton.get("ArmSelect")
        self.button_led_writer.set_button_colour(arm_select_button, Colours.off)
        for function in self.button_functions:
            button = self.product_defs.FunctionToButton.get(function)
            self.button_led_writer.set_button_colour(button, Colours.off)
