import flet as ft

from chaewon_login.routing.route_data import PageRoute
from chaewon_login.ui.components.dialogs import confirm_logout_dialog
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.containers import default_column, default_container
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
