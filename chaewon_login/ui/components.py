import flet as ft

from chaewon_login.ui.styles import *
from enum import Enum
from typing import Callable, Any

class InputFieldType(Enum):
    USERNAME = "username"
    PASSWORD = "password"

class TextType(Enum):
    TITLE = "title"
    SUBTITLE = "subtitle"
    DEFAULT = "default"

def default_text(input_type: TextType, input_text: str) -> ft.Text:
    if input_type == TextType.TITLE:
        return ft.Text(
            value=input_text,
            style=default_title_style,
            text_align=ft.TextAlign.CENTER
        )
    elif input_text == TextType.SUBTITLE:
        return ft.Text(
            value=input_text,
            style=default_subtitle_style,
            text_align=ft.TextAlign.CENTER
        )
    elif input_text == TextType.DEFAULT:
        return ft.Text(
            value=input_text,
            style=default_text_style,
            text_align=ft.TextAlign.CENTER
        )
    else:
        raise ValueError(f"Unsupported input type: {input_type}")

def default_input_field(input_type: InputFieldType) -> ft.TextField:
    if input_type == InputFieldType.USERNAME:
        return ft.TextField(
            label=f"{InputFieldType.USERNAME.value.capitalize()}",
            hint_text=f"Enter your {InputFieldType.USERNAME.value}",
            width=DEFAULT_INPUT_FIELD_WIDTH
        )
    elif input_type == InputFieldType.PASSWORD:
        return ft.TextField(
            label=f"{InputFieldType.PASSWORD.value.capitalize()}",
            hint_text=f"Enter your {InputFieldType.PASSWORD.value}",
            width=DEFAULT_INPUT_FIELD_WIDTH,
            password=True,
            can_reveal_password=True
        )
    else:
        raise ValueError(f"Unsupported input type: {input_type}")

def default_container(content=None):
    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        expand=True
    )

def default_column(controls=None):
    return ft.Column(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True
    )

def default_alert_dialog(
    title: ft.Text | str | None = None,
    content: ft.Control | list[ft.Control] | None = None,
    on_dismiss: Callable[[ft.AlertDialog], Any] | None = None
) -> ft.AlertDialog:
    dialog = ft.AlertDialog(
        icon=ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
        title=(
            title if isinstance(title, ft.Text)
            else ft.Text(title) if isinstance(title, str)
            else None
        ),
        title_padding=ft.padding.all(25),
        content=ft.Column(
            controls=content if isinstance(content, list) else [content] if content else [],
            tight=True
        ),
        actions_alignment=ft.MainAxisAlignment.END,
        alignment=ft.alignment.center,
        adaptive=True,
        on_dismiss=on_dismiss
    )
    return dialog
    

def test(page: ft.Page):
    page.title = "Test GUI"
    page.theme_mode = ft.ThemeMode.DARK
    
    test_username_input = default_input_field[InputFieldType.USERNAME]
    test_password_input = default_input_field[InputFieldType.PASSWORD]
    
    test_controls = [
        test_username_input,
        test_password_input
    ]
    
    test_column = default_column(controls=test_controls)
    test_container = default_container(content=test_column)
    
    page.add(test_container)
    
if __name__ == "__main__":
    ft.app(target=test)