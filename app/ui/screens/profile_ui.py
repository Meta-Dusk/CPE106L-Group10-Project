import flet as ft

from app.routing.route_data import PageRoute
from app.db.db_manager import find_user
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.components.containers import div
from app.ui.screens.shared_ui import render_page, preset_logout_button
from app.assets.images import default_image, ImageData


def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)

    if user_doc:
        title = default_text(DefaultTextStyle.TITLE, f"👤 | {user_doc['username']}'s Profile")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, "Welcome back!")
    else:
        title = default_text(DefaultTextStyle.TITLE, "User not found 😢")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, f"User ID: {user_id}")

    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)
    image = default_image()
    image.src = ImageData.CHAEWON_SIDE.value.path

    buttons = ft.Row(
        controls=[logout_btn, back_btn],
        alignment=ft.MainAxisAlignment.END
    )

    render_page(page, [title, image, subtitle, div(), buttons])
