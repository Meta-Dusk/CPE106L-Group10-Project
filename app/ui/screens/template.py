"""
This is a template that you can just copy-paste when making a new navigatable page.
The UI elements provided are for uniformity of all pages, having the most basic of
capabilities per page (Toggleable theme mode, and the basic control buttons).
"""

import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.components.containers import div, default_row, spaced_buttons
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme,
    preset_exit_button)
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.routing.route_data import PageRoute


def handle_template(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "Example template.")
    
    # Logo setup
    logo = set_logo()                       # Get the default logo
    toggleable_logo = container_setup(logo) # Put the logo into an container ready for animation
    
    # Animation handler; only put interactable buttons in the `toggle_controls` parameter.
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, theme_toggle],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click) # Use the preset theme toggle button
    
    logout_btn = preset_logout_button(page)                         # Use the preset logout button
    
    # The `preset_button()` function is meant for static button definitions that're commonly used, such as:
    # logout, back, cancel, etc. If you're going to make a custom button that will only be used once, just
    # use the `default_action_button()` function instead.
    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=lambda e: page.go(PageRoute.DASHBOARD.value)
    )
    exit_btn = preset_exit_button()
    
    control_buttons = default_row([logout_btn, back_btn])      # Put optional controls here
    top_row = spaced_buttons([exit_btn], [theme_toggle])       # Put essential controls here
    
    # The purpose of `render_page()` is to just put the provided list of controls into a `default_container()`,
    # so you can just insert directly these controls. Just don't put a row inside of a column, since that will
    # not work. Doing it the other way around also doesn't work.
    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title,
        # <- Insert here your main UI elements
        div(),
        control_buttons
    ])