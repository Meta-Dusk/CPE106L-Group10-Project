import flet as ft

from enum import Enum
from chaewon_login.ui.styles import (
    default_text_style, default_subtitle_style,
    default_title_style, default_error_text_style,
    DEFAULT_INPUT_FIELD_WIDTH)


# TODO: Refactor default text types to implement new data structure, as seen in `images.py`
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
    width: int = DEFAULT_INPUT_FIELD_WIDTH,
    auto_focus: bool = False,
    password: bool = False,
    can_reveal_password: bool = False
) -> ft.TextField:
    if input_type == InputFieldType.USERNAME:
        auto_focus=True
    elif input_type == InputFieldType.PASSWORD:
        password=True,
        can_reveal_password=True
        
    return ft.TextField(
        label=f"{input_type.value.capitalize()}",
        hint_text=f"Enter your {input_type.value}",
        width=width,
        autofocus=auto_focus,
        password=password,
        can_reveal_password=can_reveal_password
    )
    
uri_input_field = ft.TextField(
    label="MongoDB URI",
    hint_text="Input the full connection string here",
    width=500,
    password=True,
    can_reveal_password=True
)