from script.actions import MixerBankChangeAttemptedAction, MixerBankChangedAction
from script.constants import Pots, ScrollingSpeed
from script.device_independent.util_view import View
from script.device_independent.util_view.scrolling_arrow_button_view import ScrollingArrowButtonView
from script.fl_constants import DockSide
from script.fl_utils import FlUtils


class MixerBankButtonView(View):
    tracks_per_bank = Pots.Num.value
    first_mixer_track_index = 1

    def __init__(self, action_dispatcher, button_led_writer, fl, product_defs, model):
        super().__init__(action_dispatcher)
        self.fl = fl
        self.fl_utils = FlUtils(fl)
        self.model = model
        self.arrow_button_view = ScrollingArrowButtonView(
            action_dispatcher,
            button_led_writer,
            product_defs,
            decrement_button="MixerBankLeft",
            increment_button="MixerBankRight",
            on_page_changed=self._on_page_changed,
            on_page_change_attempted=self._on_page_change_attempt,
            speed=ScrollingSpeed.Slow.value,
        )

    def _on_show(self):
        if self.model.mixer_track_active_bank is None:
            self.model.mixer_track_active_bank = self._get_first_bank_in_center_dock_if_exists()
        self.arrow_button_view.set_page_range(0, self.model.mixer_track_active_bank)
        self.arrow_button_view.set_active_page(self.model.mixer_track_active_bank)
        self._handle_docked_tracks_changed()
        self._update_mixer_bank_state(
            self.model.mixer_track_active_bank, self._get_all_tracks_in_displayed_order_per_dockside()
        )
        self.arrow_button_view.show()

    def _on_hide(self):
        self.arrow_button_view.hide()

    def _on_page_changed(self):
        self.model.mixer_track_active_bank = self.arrow_button_view.active_page
        self._update_mixer_bank_state(
            self.model.mixer_track_active_bank, self._get_all_tracks_in_displayed_order_per_dockside()
        )
        self.action_dispatcher.dispatch(MixerBankChangedAction())

    def _on_page_change_attempt(self):
        self.action_dispatcher.dispatch(MixerBankChangeAttemptedAction())

    def _handle_docked_tracks_changed(self):
        tracks_per_dockside = self._get_all_tracks_in_displayed_order_per_dockside()
        self._update_num_banks(tracks_per_dockside)

    def _calculate_num_banks_in_dock(self, tracks_in_dock):
        return (len(tracks_in_dock) + self.tracks_per_bank - 1) // self.tracks_per_bank

    def _get_first_bank_in_center_dock_if_exists(self):
        tracks_per_dockside = self._get_all_tracks_in_displayed_order_per_dockside()
        num_left_banks, num_center_banks, num_right_banks = [
            self._calculate_num_banks_in_dock(tracks) for tracks in tracks_per_dockside
        ]
        return num_left_banks if num_center_banks > 0 else 0

    def _update_mixer_bank_state(self, bank, tracks_per_dockside):
        num_banks_per_dock = [self._calculate_num_banks_in_dock(tracks) for tracks in tracks_per_dockside]

        tracks_in_current_dock = []
        bank_in_current_dock = bank
        for num_banks, tracks in zip(num_banks_per_dock, tracks_per_dockside):
            if bank_in_current_dock < num_banks:
                tracks_in_current_dock = tracks
                break
            bank_in_current_dock = bank_in_current_dock - num_banks

        first_index = bank_in_current_dock * self.tracks_per_bank
        last_index = first_index + self.tracks_per_bank - 1
        self.model.mixer_tracks_in_active_bank = tracks_in_current_dock[first_index : last_index + 1]

    def _update_num_banks(self, tracks_per_dockside):
        num_banks = 0
        for tracks_in_dock in tracks_per_dockside:
            num_banks_in_dock = self._calculate_num_banks_in_dock(tracks_in_dock)
            num_banks = num_banks + num_banks_in_dock

        self.arrow_button_view.set_page_range(first_page=0, last_page=num_banks - 1)
        self._on_page_changed()

    def _get_all_tracks_in_displayed_order_per_dockside(self):
        tracks_for_left_dock = self.fl_utils.get_mixer_tracks_for_dock_side(DockSide.Left.value)
        tracks_for_center_dock = self.fl_utils.get_mixer_tracks_for_dock_side(DockSide.Center.value)
        tracks_for_right_dock = self.fl_utils.get_mixer_tracks_for_dock_side(DockSide.Right.value)
        return [
            tracks_for_left_dock,
            tracks_for_center_dock,
            tracks_for_right_dock,
        ]

    def handle_AllMixerTracksChangedAction(self, action):
        self._handle_docked_tracks_changed()
