import flet as ft

from chaewon_login.ui.components.containers import default_column
from typing import Callable, Optional
from chaewon_login.ui.styles import default_action_button_style
from enum import Enum


def launch_mode_radio_choice(
    value: str | None = None,
    label: str | ft.Text | None = "Launch Mode",
    label_style: Optional[ft.TextStyle] = None,
    fill_color: ft.ControlStateValue[ft.Colors] = ft.Colors.PRIMARY_CONTAINER
) -> ft.Radio:
    return ft.Radio(
        value=value,
        label=label,
        label_style=label_style or ft.TextStyle(color=ft.Colors.ON_PRIMARY_CONTAINER),
        fill_color=fill_color,
        autofocus=True,
        active_color=ft.Colors.PRIMARY_CONTAINER,
        splash_radius=15
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
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Action button pressed! {f.text}"),
    style: ft.ButtonStyle = default_action_button_style,
    icon: ft.IconValue = None
) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        width=120,
        style=style,
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.ON_PRIMARY,
        icon=icon
    )
    
# == Preset Buttons ==
class DefaultButton(Enum):
    CANCEL = "Cancel"
    OKAY = "Okay"
    LAUNCH = "Launch"
    LOGOUT = "Log Out"
    LOGIN = "Log In"
    
def preset_button(
    type: DefaultButton,
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"{DefaultButton.value} button pressed! {f.text}"),
    preset_icon: ft.IconValue = None
) -> ft.ElevatedButton:
    if type == DefaultButton.LOGOUT:
        preset_icon = ft.Icons.LOGOUT
    elif type == DefaultButton.LOGIN:
        preset_icon = ft.Icons.LOGIN
    
    return default_action_button(
        text=type.value,
        on_click=on_click,
        icon=preset_icon
    )
    
def cancel_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Cancel button pressed! {f.text}")
) -> ft.ElevatedButton:
    return default_action_button(
        text="Cancel",
        on_click=on_click,
    )
    
def launch_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Launch button pressed! {f.text}")
) -> ft.ElevatedButton:
    return default_action_button(
        text="Launch",
        on_click=on_click,
    )
    
def okay_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Okay button pressed! {f.text}")
) -> ft.ElevatedButton:
    return default_action_button(
        text="Okay",
        on_click=on_click,
    )
    
def logout_button(
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Logout button pressed! {f.text}")
) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text="Log Out",
        icon=ft.Icons.LOGOUT,
        on_click=on_click,
        bgcolor=ft.Colors.RED_400,
        color=ft.Colors.WHITE
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
    