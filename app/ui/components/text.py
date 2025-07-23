import flet as ft

from app.ui.styles import DefaultTextStyle, DefaultInputFieldType, InputFieldConfig


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

def default_input_field(
    input_field_type: DefaultInputFieldType,
    label: str | None = None
) -> ft.TextField:
    config = input_field_type.value
    return ft.TextField(
        label=config.label if label is None else label,
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
    label: str,
    input_field_type: DefaultInputFieldType | None = None,
    is_password: bool = False,
    read_only: bool = False,
    hint_text: str | None = None,
    suffix: ft.Control | None = None,
    on_change: ft.OptionalControlEventCallable = None,
    prefix_text: str | None = None,
    max_length: int | None = None,
    keyboard_type: ft.KeyboardType | None = None
) -> ft.TextField:
    config = input_field_type.value if input_field_type is not None else DefaultInputFieldType.DEFAULT.value
    generated_hint = hint_text or f"Please enter your {label.lower()} here."
    
    return ft.TextField(
        label=label,
        label_style=config.label_style,
        width=config.width,
        height=config.height,
        autofocus=config.auto_focus,
        password=is_password,
        can_reveal_password=is_password,
        selection_color=config.selection_color,
        bgcolor=config.bg_color,
        color=config.color,
        hint_text=generated_hint,
        hint_style=config.hint_style,
        border_radius=config.border_radius,
        adaptive=config.adaptive,
        size_constraints=config.size_constraints,
        expand=config.expand,
        read_only=read_only,
        suffix=suffix,
        on_change=on_change,
        prefix_text=prefix_text,
        max_length=max_length,
        keyboard_type=keyboard_type
    )