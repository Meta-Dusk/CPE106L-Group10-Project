import flet as ft

from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.containers import div, default_row
from chaewon_login.ui.screens.shared_ui import render_page, preset_logout_button
from chaewon_login.assets.images import default_image, ImageData
from chaewon_login.routing.route_data import PageRoute


def handle_viewgraphs(page: ft.Page, _):
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")

    msg = default_text(TextType.TITLE, "You are now viewing graphs 🤨")
    image = default_image()
    image.src = ImageData.CHAEWON_SAD.value.path
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile)
    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    
    control_buttons = default_row(controls=[profile_btn, logout_btn, back_btn])

    render_page(page, [msg, image, div(), control_buttons])