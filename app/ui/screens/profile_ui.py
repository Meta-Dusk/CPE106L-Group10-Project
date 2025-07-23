import flet as ft
import asyncio

from app.routing.route_data import PageRoute
from app.db.db_manager import find_user
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.components.containers import div, default_row
from app.ui.screens.shared_ui import render_page, preset_logout_button, toggle_theme, theme_toggle_button
from app.assets.images import set_logo
from app.ui.animations import container_setup
from app.utils import enable_control_after_delay


def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)

    if user_doc:
        title = default_text(DefaultTextStyle.TITLE, f"{user_doc['username']}'s Profile")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, "Welcome back!" if not user_doc['op'] else "Greetings, admin.")
    else:
        title = default_text(DefaultTextStyle.TITLE, "User not found 😢")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, f"User ID: {user_id}")
    
    column = ft.Column(
        controls=[
            default_text(DefaultTextStyle.DEFAULT, "Enter full name here"),
            default_text(DefaultTextStyle.DEFAULT, "Enter home address"),
            default_text(DefaultTextStyle.DEFAULT, "Enter date of birth"),
            default_text(DefaultTextStyle.DEFAULT, "Enter nationality"),
            default_text(DefaultTextStyle.DEFAULT, "Enter phone number"),
            default_text(DefaultTextStyle.DEFAULT, "Enter active email"),
            default_text(DefaultTextStyle.DEFAULT, "Insert verification status"),
            default_text(DefaultTextStyle.DEFAULT, "Button for driver application")
        ],
        expand=True,
        run_alignment=ft.MainAxisAlignment.CENTER,
        run_spacing=10
    )
    container = ft.Container(
        content=column,
        bgcolor=ft.Colors.ON_SURFACE,
        expand=True
    )
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def mod_toggle_theme(e, delay: float = 2.0):
        asyncio.create_task(enable_control_after_delay(control_buttons, delay))
        await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
        
    theme_toggle = theme_toggle_button(on_click=mod_toggle_theme)

    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)

    control_buttons = default_row(controls=[logout_btn, back_btn])

    render_page(page, [
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        subtitle,
        container,
        div(),
        control_buttons
    ])
