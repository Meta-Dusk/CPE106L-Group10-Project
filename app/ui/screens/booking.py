import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import (
    preset_button, DefaultButton, default_action_button, reactive_text_button)
from app.ui.components.containers import div, default_row, default_column, spaced_buttons
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme, preset_exit_button)
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.routing.route_data import PageRoute


def handle_booking(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "Book a Ride?")
    title_container = ft.Container(
        content=title,
        alignment=ft.alignment.center,
        adaptive=True,
        border_radius=20,
        padding=10,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        expand=True
    )
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, theme_toggle],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    
    logout_btn = preset_logout_button(page)
    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=lambda e: page.go(PageRoute.DASHBOARD.value)
    )
    
    exit_btn = preset_exit_button(page)
    
    book_nearby_btn = default_action_button(
        text="Book Nearby Drivers",
        icon=ft.Icons.DIRECTIONS_CAR,
        tooltip="Attempt to book a nearby driver",
        width=250,
        expand=True
    )
    
    buttons_container = ft.Container(
        content=book_nearby_btn,
        alignment=ft.alignment.center,
        adaptive=True,
        border_radius=20,
        padding=10,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        expand=True
    )
    
    control_buttons = default_row([logout_btn, back_btn])
    
    top_row = spaced_buttons([exit_btn], [theme_toggle])
    
    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title_container,
        buttons_container,
        div(),
        control_buttons
    ])