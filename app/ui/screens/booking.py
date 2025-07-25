import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row, default_column, spaced_buttons
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme, preset_exit_button)
from app.ui.styles import build_action_button_style
from app.ui.animations import container_setup
from app.assets.images import generate_random_image, update_image_with_random, set_logo
from app.routing.route_data import PageRoute


def handle_booking(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "Book a Ride?")
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[example_buttons, control_buttons, theme_toggle],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    
    random_image = generate_random_image()
    container_text = ft.Text(
        value="I AM AN EXAMPLE 😔🤚",
        color=ft.Colors.ON_PRIMARY_CONTAINER,
        text_align=ft.TextAlign.CENTER,
        size=40
    )
    
    # If you want a custom container for future stuff, you can just do this:
    example_container = ft.Container(
        content=default_column([
            container_text,
            random_image
        ]),
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        alignment=ft.alignment.center,
        adaptive=True,
        expand=True,
        width=800,
        height=400
    )
    
    logout_btn = preset_logout_button(page)
    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=lambda e: page.go(PageRoute.DASHBOARD.value)
    )
        
    test_btn = default_action_button(
        text="Button with custom button style 🤨",
        icon=ft.Icons.INFO,
        style=build_action_button_style(
            primary=ft.Colors.BLACK,
            on_primary=ft.Colors.WHITE,
            primary_highlight=ft.Colors.AMBER,
            seconday_highlight=ft.Colors.GREEN
        ),
        tooltip="I don't do anything 😏",
        on_click=lambda e: update_image_with_random(random_image)
    )
    
    exit_btn = preset_exit_button(page)
    
    example_buttons = default_row([test_btn])
    control_buttons = default_row([logout_btn, back_btn])
    
    top_row = spaced_buttons([exit_btn], [theme_toggle])
    
    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title,
        example_container,
        div(),
        example_buttons,
        control_buttons
    ])