import flet as ft

from enum import Enum
from chaewon_login.ui.styles import (
    default_text_style,
    default_subtitle_style,
    default_title_style,
    default_error_text_style,
    DEFAULT_INPUT_FIELD_WIDTH
)


class TextType(Enum):
    TITLE = "title"
    SUBTITLE = "subtitle"
    DEFAULT = "default"
    ERROR = "error"

def default_text(
    input_type: TextType,
    input_text: str | None = None
) -> ft.Text:
    styled_text = ft.Text(
        value=input_text,
        text_align=ft.TextAlign.CENTER
    )
    if input_type == TextType.TITLE:
        styled_text.style = default_title_style
        return styled_text
    elif input_type == TextType.SUBTITLE:
        styled_text.style = default_subtitle_style
        return styled_text
    elif input_type == TextType.DEFAULT:
        styled_text.style = default_text_style
        return styled_text
    elif input_type == TextType.ERROR:
        styled_text.style = default_error_text_style
        return styled_text
    else:
        raise ValueError(f"Unsupported input type: {input_type}")
    
    
class InputFieldType(Enum):
    USERNAME = "username"
    PASSWORD = "password"

def default_input_field(
    input_type: InputFieldType = InputFieldType.USERNAME,
    width: int = DEFAULT_INPUT_FIELD_WIDTH
) -> ft.TextField:
    if input_type == InputFieldType.USERNAME:
        return ft.TextField(
            label=f"{InputFieldType.USERNAME.value.capitalize()}",
            hint_text=f"Enter your {InputFieldType.USERNAME.value}",
            width=width,
            autofocus=True
        )
    elif input_type == InputFieldType.PASSWORD:
        return ft.TextField(
            label=f"{InputFieldType.PASSWORD.value.capitalize()}",
            hint_text=f"Enter your {InputFieldType.PASSWORD.value}",
            width=width,
            password=True,
            can_reveal_password=True
        )
    else:
        raise ValueError(f"Unsupported input type: {input_type}")
    
uri_input_field = ft.TextField(
    label="MongoDB URI",
    hint_text="Input the full connection string here",
    width=500,
    password=True,
    can_reveal_password=True
)