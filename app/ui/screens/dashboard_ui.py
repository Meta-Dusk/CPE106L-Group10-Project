import flet as ft
import asyncio

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row, default_column
from app.ui.animations import container_setup
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, toggle_theme, theme_toggle_button, open_profile)
from app.assets.images import set_logo
from app.routing.route_data import PageRoute
from app.utils import enable_control_after_delay


def handle_dashboard(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "This is the dashboard 😔🤚")
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def mod_toggle_theme(e, delay: float = 2.0):
        asyncio.create_task(enable_control_after_delay(control_buttons, delay))
        asyncio.create_task(enable_control_after_delay(other_buttons, delay))
        asyncio.create_task(enable_control_after_delay(theme_toggle, delay))
        await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
        
    theme_toggle = theme_toggle_button(on_click=mod_toggle_theme)
    
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile(page))
    
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
    
    api_key_btn = default_action_button(
        text="API Key",
        icon=ft.Icons.KEY,
        on_click=lambda e: page.go(PageRoute.API_KEY.value),
        tooltip="Configure API key settings"
    )
    
    control_buttons = default_row(controls=[profile_btn, logout_btn])
    other_buttons = default_row(controls=[mathplot_btn, booking_btn, api_key_btn])
    
    form = default_column([
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        other_buttons,
        control_buttons
    ])

    render_page(page, form)


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