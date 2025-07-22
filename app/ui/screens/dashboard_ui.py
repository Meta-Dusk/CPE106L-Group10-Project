import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row
from app.ui.screens.shared_ui import render_page, preset_logout_button
from app.assets.images import default_image
from app.routing.route_data import PageRoute


def handle_dashboard(page: ft.Page, _):
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")

    msg = default_text(DefaultTextStyle.TITLE, "This is the dashboard 😔🤚")
    image = default_image()
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile)
    mathplot_btn = default_action_button(
        text="View Plots",
        icon=ft.Icons.AUTO_GRAPH,
        on_click=lambda e: page.go(PageRoute.GRAPHS.value),
        tooltip="Show the graphs we've been testing"
    )
    booking_btn = default_action_button(
        text="Book Now",
        icon=ft.Icons.CAR_RENTAL,
        on_click=lambda e: page.go(PageRoute.BOOKING.value),
        tooltip="Show the testing screen for the booking feature"
    )
    
    control_buttons = default_row(controls=[profile_btn, logout_btn])
    other_buttons = default_row(controls=[mathplot_btn, booking_btn])

    render_page(page, [msg, image, div(), other_buttons, control_buttons])


"""
Run with `py -m app.ui.screens.dashboard_ui`.
Although it's recommended to just simply run the `launch.py` since there are issues.
"""
def test(page: ft.Page):
    page.session.set("user_id", "test_user_123")
    handle_dashboard(page, None)
    page.update()

if __name__ == "__main__":
    ft.app(target=test)