import flet as ft

from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.dialogs import confirm_logout_dialog
from chaewon_login.ui.components.containers import default_column, default_container, div
from chaewon_login.db.db_manager import find_user
from chaewon_login.routing.route_data import PageRoute
from chaewon_login.auth.user import logout_yes, logout_no


def render_page(page: ft.Page, content: ft.Control | list[ft.Control]):
    if not isinstance(content, list):
        content = [content]
    form = default_column(content)
    container = default_container(form)
    page.controls.append(container)


def preset_logout_button(page: ft.Page, page_destination: str = PageRoute.LOGIN.value) -> ft.ElevatedButton:
    def on_click(e):
        dialog = confirm_logout_dialog(
            page=page,
            yes_clicked=lambda e: logout_yes(page, dialog, page_destination),
            no_clicked=lambda e: logout_no(page, dialog)
        )
    return preset_button(DefaultButton.LOGOUT, on_click=on_click)


def dashboard_screen(page: ft.Page):
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


def profile_screen(page: ft.Page, user_id: str):
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
