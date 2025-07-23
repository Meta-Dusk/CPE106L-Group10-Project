import flet as ft

from app.ui.components.containers import default_column
from typing import Callable, Optional
from app.ui.styles import default_action_button_style, build_action_button_style
from app.utils import log_button_press
from enum import Enum
from functools import partial
from dataclasses import dataclass


class LaunchMode(Enum):
    NATIVE = "native"
    WEB = "web"
    SETUP = "setup"

DEFAULT_LAUNCH_CHOICES = [
    (LaunchMode.NATIVE.value, "Native window (default)"),
    (LaunchMode.WEB.value, "Web browser"),
    (LaunchMode.SETUP.value, "Run setup")
]

def launch_mode_radio_choice(
    value: Optional[str] = None,
    label: Optional[str | ft.Text] = "Launch Mode",
    label_style: Optional[ft.TextStyle] = None,
    fill_color: ft.ControlStateValue[ft.Colors] = ft.Colors.PRIMARY
) -> ft.Radio:
    return ft.Radio(
        value=value,
        label=label,
        label_style=label_style or ft.TextStyle(color=ft.Colors.PRIMARY),
        fill_color=fill_color,
        active_color=ft.Colors.PRIMARY,
        splash_radius=15
    )
    
def launch_mode_radio_group(
    ref: Optional[ft.Ref[ft.RadioGroup]] = None,
    choices: Optional[list[tuple[str, str]]] = None
) -> ft.RadioGroup:
    if choices is None:
        choices = choices or DEFAULT_LAUNCH_CHOICES

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
    text: Optional[str] = "Action Button",
    on_click: Callable[[ft.ElevatedButton], None] = None,
    style: ft.ButtonStyle = default_action_button_style,
    icon: ft.IconValue = None,
    width: ft.OptionalNumber = 120,
    height: ft.OptionalNumber = 40,
    auto_focus: bool = False,
    tooltip: str = None
) -> ft.ElevatedButton:
    if on_click is None:
        on_click = partial(log_button_press, text)
    
    button = ft.ElevatedButton(
        text=text,
        on_click=on_click,
        width=width,
        height=height,
        style=style,
        expand=2,
        autofocus=auto_focus,
        tooltip=tooltip
    )
    if icon:
        button.icon = icon
    return button


@dataclass
class ButtonData:
    label: str
    tooltip: str
    icon: Optional[ft.IconValue] = None

class DefaultButton(Enum):
    CANCEL = ButtonData(label="Cancel", tooltip="Cancel the current action")
    OKAY = ButtonData(label="Okay", tooltip="Confirm and proceed")
    LAUNCH = ButtonData(label="Launch", tooltip="Start the application")
    LOGOUT = ButtonData(label="Log Out", tooltip="Log out from the current session", icon=ft.Icons.LOGOUT)
    LOGIN = ButtonData(label="Log In", tooltip="Log into your account", icon=ft.Icons.LOGIN)
    REGISTER = ButtonData(label="Register", tooltip="Register a new account", icon=ft.Icons.HOW_TO_REG)
    PROFILE = ButtonData(label="My Profile", tooltip="View your profile", icon=ft.Icons.PERSON)
    BACK = ButtonData(label="Back", tooltip="Go back to the previous screen", icon=ft.Icons.KEYBOARD_RETURN)
    SUBMIT = ButtonData(label="Submit", tooltip="Submit the form data", icon=ft.Icons.CHECK)
    
def preset_button(
    type: DefaultButton,
    on_click: Callable[[ft.ElevatedButton], None] = None,
    style: ft.ButtonStyle = default_action_button_style,
    auto_focus: bool = False,
) -> ft.ElevatedButton:
    data = type.value
    
    if on_click is None:
        on_click = partial(log_button_press, data.label)
    
    return default_action_button(
        text=data.label,
        tooltip=data.tooltip,
        icon=data.icon,
        on_click=on_click,
        style=style,
        auto_focus=auto_focus,
    )

def test():
    print(LaunchMode.NATIVE.value)

if __name__ == "__main__":
    test()