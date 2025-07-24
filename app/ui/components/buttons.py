import flet as ft

from app.ui.components.containers import default_column
from typing import Callable, Optional
from app.ui.styles import default_action_button_style, RadioChoiceStyle, WindowMode
from app.utils import log_button_press
from enum import Enum
from functools import partial
from dataclasses import dataclass


class LaunchMode(Enum):
    NATIVE = "native"
    WEB = "web"
    SETUP = "setup"

DEFAULT_LAUNCH_CHOICES = [
    (LaunchMode.NATIVE.value, "Native window (default)", True),
    (LaunchMode.WEB.value, "Web browser", True),
    (LaunchMode.SETUP.value, "Run setup", True)
]

DEFAULT_WINDOW_CHOICES = [
    (WindowMode.WINDOWED.value, "Windowed (default)", True),
    (WindowMode.FULLSCREEN.value, "Full Screen", True),
    (WindowMode.BORDERLESS.value, "Borderless", True)
]

def preset_radio_choice(
    value: Optional[str] = "Value",
    label: Optional[str | ft.Text] = "Label",
    label_style: Optional[ft.TextStyle] = None,
    fill_color: ft.ControlStateValue[ft.Colors] = None,
    overlay_color: ft.ControlStateValue[ft.Colors] = None,
    active_color: ft.ColorValue = ft.Colors.PRIMARY,
    splash_radius: ft.OptionalNumber = 15,
    disabled: bool = False,
    ref: Optional[ft.Ref[ft.Radio]] = None
) -> ft.Radio:
    return ft.Radio(
        ref=ref,
        value=value,
        label=label,
        label_style=label_style or ft.TextStyle(color=ft.Colors.PRIMARY),
        fill_color=fill_color or RadioChoiceStyle.FILL_COLOR.value,
        overlay_color=overlay_color or RadioChoiceStyle.OVERLAY_COLOR.value,
        active_color=active_color,
        splash_radius=splash_radius,
        disabled=disabled
    )

def preset_radio_group(
    ref: Optional[ft.Ref[ft.RadioGroup]] = None,
    choices: Optional[list[tuple[str, str, bool]]] = None,
    selected_value: Optional[str] = None,
    radio_refs_map: Optional[dict[str, ft.Ref[ft.Radio]]] = None,
    on_change: Optional[Callable] = None
) -> ft.RadioGroup:
    if not choices:
        raise ValueError("choices must be provided and cannot be empty")

    # Find fallback if selected value is disabled
    choice_dict = {val: (lbl, enabled) for val, lbl, enabled in choices}
    is_valid_choice = lambda v: v in choice_dict and choice_dict[v][1]
    fallback_value = next((val for val, _, enabled in choices if enabled), None)

    selected = selected_value if is_valid_choice(selected_value) else fallback_value

    radios = []
    for val, lbl, enabled in choices:
        radio_ref = ft.Ref[ft.Radio]()
        if radio_refs_map is not None:
            radio_refs_map[val] = radio_ref

        radio = preset_radio_choice(
            value=val,
            label=lbl,
            disabled=not enabled,
            ref=radio_ref
        )
        if radio_refs_map is not None:
            radio_refs_map[val] = radio_ref

        radios.append(
            ft.Row(
                [radio],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    return ft.RadioGroup(
        ref=ref,
        value=selected,
        on_change=on_change,
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
    EXIT = ButtonData(label="Exit", tooltip="Close the application")
    
def preset_button(
    type: DefaultButton,
    on_click: Callable[[ft.ElevatedButton], None] = None,
    style: ft.ButtonStyle = default_action_button_style,
    auto_focus: bool = False,
) -> ft.ElevatedButton:
    data = type.value
    
    if on_click is None:
        on_click = partial(log_button_press, data.label)
    if type == DefaultButton.EXIT:
        width = 80
    else:
        width = None
    
    return default_action_button(
        text=data.label,
        tooltip=data.tooltip,
        icon=data.icon,
        on_click=on_click,
        style=style,
        auto_focus=auto_focus,
        width=width
    )

def test():
    print(LaunchMode.NATIVE.value)

if __name__ == "__main__":
    test()