import flet as ft

from chaewon_login.routing.route_data import PageRoute
from chaewon_login.db.db_manager import find_user
from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.containers import div
from chaewon_login.ui.screens.shared_ui import render_page, preset_logout_button


def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)

    if user_doc:
        title = default_text(TextType.TITLE, f"👤 | {user_doc['username']}'s Profile")
        subtitle = default_text(TextType.SUBTITLE, "Welcome back!")
    else:
        title = default_text(TextType.TITLE, "User not found 😢")
        subtitle = default_text(TextType.SUBTITLE, f"User ID: {user_id}")

    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)

    buttons = ft.Row(
        controls=[logout_btn, back_btn],
        alignment=ft.MainAxisAlignment.END
    )

    render_page(page, [title, subtitle, div(), buttons])
