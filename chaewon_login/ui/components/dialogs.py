import flet as ft
import asyncio

from typing import Callable
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.containers import default_column, default_container
from chaewon_login.ui.components.text import default_text, DefaultTextStyle


DEFAULT_TITLE_PADDING = 25

def confirm_logout_dialog(
    page: ft.Page,
    yes_clicked: Callable[[ft.ControlEvent], None],
    no_clicked: Callable[[ft.ControlEvent], None]
) -> ft.AlertDialog:
    cancel_btn = preset_button(DefaultButton.CANCEL, on_click=no_clicked)
    cancel_btn.autofocus = True
    
    dialog = ft.AlertDialog(
        modal=True,
        title=default_text(DefaultTextStyle.TITLE, "Confirm Logout"),
        content=default_text(DefaultTextStyle.SUBTITLE, "Are you sure you want to log out?"),
        actions=[
            cancel_btn,
            preset_button(DefaultButton.LOGOUT, on_click=yes_clicked)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    page.open(dialog)
    page.update()
    return dialog

    
def default_notif_dialog(
    icon: ft.IconValue | None = ft.Icon(
        name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE, size=50
    ),
    title: ft.Text | str | None = "Notif Dialog",
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
    icon: ft.IconValue | None = ft.Icon(
        name=ft.Icons.DATA_OBJECT,
        color=ft.Colors.PRIMARY,
        size=40
    ),
    title: ft.Text | str | None = "Alert Dialog",
    content: ft.Control | list[ft.Control] | None = None,
    actions: list[ft.Control] | None = None,
    page: ft.Page = None
) -> ft.AlertDialog:
    def close_dialog(e):
        page.close(dialog)
        page.update()

    dialog = ft.AlertDialog(
        icon=icon,
        modal=True,
        adaptive=True,
        scrollable=True,
        title=default_text(DefaultTextStyle.TITLE,input_text=title) if isinstance(title, str) else title,
        title_padding=ft.padding.all(DEFAULT_TITLE_PADDING),
        content=default_column(
            controls=content if isinstance(content, list) else [content] if content else []
        ),
        actions=actions or [preset_button(DefaultButton.OKAY,on_click=close_dialog)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.PRIMARY_CONTAINER
    )
    
    return dialog

def error_dialog(
    icon: ft.IconValue | None = ft.Icon(
        name=ft.Icons.ERROR,
        color=ft.Colors.ERROR,
        size=30
    ),
    content: ft.Control | list[ft.Control] | None = None,
    page: ft.Page = None
) -> ft.AlertDialog:
    def close_dialog(e):
        page.close(dialog)
        page.update()
    okay_btn = preset_button(DefaultButton.OKAY,on_click=close_dialog)
    okay_btn.color = ft.Colors.ON_ERROR
    okay_btn.bgcolor = ft.Colors.ERROR
    title = default_text(DefaultTextStyle.ERROR, input_text="ERROR")
    title.size = 25
    
    dialog = ft.AlertDialog(
        icon=icon,
        modal=True,
        adaptive=True,
        scrollable=True,
        title=title,
        title_padding=ft.padding.all(10),
        content=default_column(
            controls=content if isinstance(content, list) else [content] if content else []
        ),
        content_padding=ft.padding.all(0),
        actions=[okay_btn],
        actions_padding=ft.padding.all(10),
        actions_alignment=ft.MainAxisAlignment.CENTER,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.ERROR_CONTAINER
    )
    
    return dialog

    
# == Dialog Functions ==
async def show_auto_closing_dialog(
    page: ft.Page,
    dialog: ft.AlertDialog,
    duration: float = 3.0
):
    page.open(dialog)
    page.update()

    await asyncio.sleep(duration)

    page.close(dialog)
    page.update()
    
    
"""
Run dialogs.py to test the preset dialogs.
Use the following command to run:
py -m chaewon_login.ui.components.dialogs
"""
    
def test(page: ft.Page):
    from chaewon_login.ui.styles import apply_default_page_config
    
    apply_default_page_config(page)
    
    test_text = default_text(DefaultTextStyle.SUBTITLE, "Test")
    test_container = default_container(test_text)
    dialog = default_alert_dialog(content=test_text, page=page)
    
    page.add(test_container)
    page.open(dialog)
    page.update()
    
    # asyncio.run(show_auto_closing_dialog(page=page, dialog=dialog))

if __name__ == "__main__":
    ft.app(target=test)