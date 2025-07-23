import flet as ft

from app.ui.styles import DefaultTextStyle, DefaultInputFieldType


def default_text(
    text_type: DefaultTextStyle,
    text: ft.OptionalString = None,
    text_align: ft.TextAlign = ft.TextAlign.CENTER
) -> ft.Text:
    style = text_type.value
    return ft.Text(
        value=text,
        style=ft.TextStyle(
            font_family=style.font_family,
            size=style.size,
            weight=style.weight,
            color=style.color
        ),
        text_align=text_align
    )

def default_input_field(input_field_type: DefaultInputFieldType) -> ft.TextField:
    config = input_field_type.value
    return ft.TextField(
        label=config.label,
        label_style=config.label_style,
        width=config.width,
        height=config.height,
        autofocus=config.auto_focus,
        password=config.password,
        can_reveal_password=config.can_reveal_password,
        selection_color=config.selection_color,
        bgcolor=config.bg_color,
        color=config.color,
        hint_text=config.hint_text,
        hint_style=config.hint_style,
        border_radius=config.border_radius,
        adaptive=config.adaptive,
        size_constraints=config.size_constraints,
        expand=config.expand
    )

def mod_input_field(
    input_field_type: DefaultInputFieldType,
    **kwargs
) -> ft.TextField:
    """Modified input field that allows customization through kwargs"""
    field = default_input_field(input_field_type)
    
    # Apply any additional modifications
    for key, value in kwargs.items():
        if hasattr(field, key):
            setattr(field, key, value)
    
    return field
