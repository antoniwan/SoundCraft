from script.device_independent.util_view.arrow_button_view import ArrowButtonView
from util.plain_data import PlainData


class PagedLayoutManager:
    @PlainData
    class Layout:
        layout_id: int
        notification_primary: str
        notification_secondary: str
        views: list

    def __init__(
        self,
        action_dispatcher,
        product_defs,
        screen_writer,
        button_led_writer,
        layouts,
        page_up_function,
        page_down_function,
    ):
        self.screen_writer = screen_writer
        self.layouts = layouts
        self.arrow_button_view = ArrowButtonView(
            action_dispatcher,
            button_led_writer,
            product_defs,
            decrement_button=page_up_function,
            increment_button=page_down_function,
            last_page=len(self.layouts) - 1,
            on_page_changed=self._on_page_changed,
        )
        self.active_layout_index = None

    def show(self):
        if self.active_layout_index is None:
            self.active_layout_index = 0
            self.on_layout_selected(self._active_layout.layout_id)

        self.arrow_button_view.show()
        self._show_layout_views()

    def hide(self):
        self._hide_layout_views()
        self.arrow_button_view.hide()
        self.active_layout_index = None

    def on_layout_selected(self, layout_id):
        pass

    @property
    def active_layout(self):
        return self._active_layout.layout_id

    def set_layout(self, layout_id):
        index = next(index for index, layout in enumerate(self.layouts) if layout.layout_id == layout_id)
        self.arrow_button_view.set_active_page(index)
        self.active_layout_index = index

    def _show_layout_views(self):
        for view in self._active_layout.views:
            view.show()

    def _hide_layout_views(self):
        if self.active_layout_index is None:
            return

        for view in self._active_layout.views:
            view.hide()

    def _on_page_changed(self):
        self._set_active_layout_index(self.arrow_button_view.active_page)
        self.on_layout_selected(self._active_layout.layout_id)

    @property
    def _active_layout(self):
        return self.layouts[self.active_layout_index]

    def _set_active_layout_index(self, index):
        self._hide_layout_views()

        self.active_layout_index = index

        self._show_layout_views()
        self.screen_writer.display_notification(
            self._active_layout.notification_primary, self._active_layout.notification_secondary
        )
