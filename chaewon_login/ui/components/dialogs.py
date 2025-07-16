import flet as ft

from chaewon_login.ui.route_data import PageRoute
from typing import Callable
from chaewon_login.ui.components.buttons import (
    okay_button,
    default_action_button,
    cancel_button
)


DEFAULT_TITLE_PADDING = 25

def confirm_logout_dialog(
    page: ft.Page,
    yes_clicked: Callable[[ft.ControlEvent], None],
    no_clicked: Callable[[ft.ControlEvent], None]
) -> ft.AlertDialog:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Logout"),
        content=ft.Text("Are you sure you want to log out?"),
        actions=[
            cancel_button(
                on_click=no_clicked,
                bg_color=ft.Colors.GREY
            ),
            default_action_button(
                text="Log Out",
                on_click=yes_clicked,
                bg_color=ft.Colors.RED
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(dialog)
    page.update()
    return dialog

    
def default_notif_dialog(
    icon: ft.Icon | None = ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
    title: ft.Text | str | None = "Alert Dialog",
    content: ft.Control | list[ft.Control] | None = None,
    on_dismiss: Callable[[ft.AlertDialog], None] | None = None
) -> ft.AlertDialog:
    dialog = ft.AlertDialog(
        icon=icon,
        title=(
            title if isinstance(title, ft.Text)
            else ft.Text(title) if isinstance(title, str)
            else None
        ),
        title_padding=ft.padding.all(DEFAULT_TITLE_PADDING),
        content=ft.Column(
            controls=content if isinstance(content, list) else [content] if content else [],
            tight=True
        ),
        alignment=ft.alignment.center,
        adaptive=True,
        on_dismiss=on_dismiss
    )
    return dialog

def default_alert_dialog(
    icon: ft.Icon | None = ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
    title: ft.Text | str | None = "Alert Dialog",
    content: ft.Control | list[ft.Control] | None = None,
    actions: list[ft.Control] | None = None,
) -> ft.AlertDialog:
    dialog = ft.AlertDialog()

    def close_dialog(e):
        dialog.open = False
        dialog.update()

    dialog = ft.AlertDialog(
        icon=icon,
        modal=True,
        title=ft.Text(title) if isinstance(title, str) else title,
        title_padding=ft.padding.all(DEFAULT_TITLE_PADDING),
        content=ft.Column(
            controls=content if isinstance(content, list) else [content] if content else [],
            tight=True
        ),
        actions=actions or [okay_button(on_click=close_dialog)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        alignment=ft.alignment.center,
        adaptive=True,
    )