import flet as ft

from chaewon_login.ui.components.containers import default_column
from typing import Callable, Optional
from chaewon_login.ui.styles import default_text_style, default_action_button_style

def launch_mode_radio_choice(
    value: str | None = None,
    label: str | ft.Text | None = "Launch Mode",
    label_style: Optional[ft.TextStyle] = None,
    fill_color: ft.ControlStateValue[ft.Colors] = ft.Colors.WHITE
) -> ft.Radio:
    return ft.Radio(
        value=value,
        label=label,
        label_style=label_style or default_text_style,
        fill_color=fill_color,
        autofocus=True
    )
    
def launch_mode_radio_group(
    ref: Optional[ft.Ref[ft.RadioGroup]] = None,
    choices: list[tuple[str, str]] = None
) -> ft.RadioGroup:
    if choices is None:
        choices = [
            ("native", "Native window (default)"),
            ("web", "Web browser"),
            ("setup", "Run setup")
        ]

    radios = [
        ft.Row(
            [launch_mode_radio_choice(value=val, label=lbl)],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        for val, lbl in choices
    ]

    return ft.RadioGroup(
        ref=ref,
        value=choices[0][0],
        content=default_column(controls=radios)
    )


    
def default_action_button(
    text: str | None = "Action Button",
    on_click: Callable[[ft.Control], None] = lambda f: print(f"Action button pressed! {f.text}"),
    bg_color: ft.ColorValue = ft.Colors.WHITE,
    color: ft.ColorValue = ft.Colors.BLACK
) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        bgcolor=bg_color,
        color=color,
        width=120,
        style=default_action_button_style
    )
    
def cancel_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Cancel button pressed! {f.text}"),
    bg_color: ft.Colors = ft.Colors.RED
) -> ft.ElevatedButton:
    return default_action_button(
        text="Cancel",
        on_click=on_click,
        bg_color=bg_color
    )
    
def launch_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Launch button pressed! {f.text}")
) -> ft.ElevatedButton:
    return default_action_button(
        text="Launch",
        on_click=on_click,
        bg_color=ft.Colors.GREEN
    )
    
def okay_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Okay button pressed! {f.text}")
) -> ft.ElevatedButton:
    return default_action_button(
        text="Okay",
        on_click=on_click,
        bg_color=ft.Colors.GREEN
    )
    
def profile_button(page: ft.Page):
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")
            
    return ft.ElevatedButton(
        text="Go to My Profile",
        icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        on_click=open_profile
    )
    
