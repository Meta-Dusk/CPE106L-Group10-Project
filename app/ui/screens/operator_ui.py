import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.components.containers import div, default_row, spaced_buttons
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme, preset_exit_button,
    open_profile)
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.db.db_manager import find_user

# TODO: Implement Admin controls for: driver and user verification.
def handle_operator(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)
    
    if user_doc:
        subtitle = default_text(DefaultTextStyle.SUBTITLE, "ADMIN ONLY!" if not user_doc['op'] else f"Greetings, {user_doc['username']}")
    else:
        subtitle = default_text(DefaultTextStyle.SUBTITLE, f"Error_User_ID: {user_id}")
    
    title = default_text(DefaultTextStyle.TITLE, "OPERATOR ONLY CONTROL CENTER")
    
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
        on_click=open_profile(page)
    )
    exit_btn = preset_exit_button(page)
    
    control_buttons = default_row([logout_btn, back_btn])
    top_row = spaced_buttons([exit_btn], [theme_toggle])
    
    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title,
        subtitle,
        div(),
        control_buttons
    ])