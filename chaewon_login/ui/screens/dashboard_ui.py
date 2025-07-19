import flet as ft

from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.containers import div
from chaewon_login.ui.screens.shared_ui import render_page, preset_logout_button


def handle_dashboard(page: ft.Page, _):
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")

    msg = default_text(TextType.TITLE, "This is the dashboard 😔🤚")
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile)

    buttons = ft.Row(
        controls=[profile_btn, logout_btn],
        alignment=ft.MainAxisAlignment.END
    )

    render_page(page, [msg, div(), buttons])
