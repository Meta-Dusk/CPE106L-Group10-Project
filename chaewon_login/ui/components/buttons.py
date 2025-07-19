import flet as ft

from chaewon_login.ui.components.containers import default_column
from typing import Callable, Optional
from chaewon_login.ui.styles import default_action_button_style, build_action_button_style
from enum import Enum


def launch_mode_radio_choice(
    value: Optional[str] = None,
    label: Optional[str | ft.Text] = "Launch Mode",
    label_style: Optional[ft.TextStyle] = None,
    fill_color: ft.ControlStateValue[ft.Colors] = ft.Colors.PRIMARY_CONTAINER
) -> ft.Radio:
    return ft.Radio(
        value=value,
        label=label,
        label_style=label_style or ft.TextStyle(color=ft.Colors.ON_PRIMARY_CONTAINER),
        fill_color=fill_color,
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
    text: Optional[str] = "Action Button",
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"Action button pressed! {f}"),
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
        icon=icon,
        expand=2
    )
  
# TODO: Finish transferring components from login_ui.py here
  
# def db_toggle_button(
#     current_mode,
#     text_switch_to_sqlite,
#     text_switch_to_mongo,
    
# ):
#     return ft.TextButton(
#         icon=ft.Icons.CODE_SHARP,
#         icon_color=ft.Colors.PRIMARY,
#         text=text_switch_to_sqlite if current_mode == DBMode.MONGO.value else text_switch_to_mongo,
#         tooltip="Switch between available databases",
#         on_click=handle_db_toggle
#     )
    
    
# == Preset Buttons ==
class DefaultButton(Enum):
    CANCEL = "Cancel"
    OKAY = "Okay"
    LAUNCH = "Launch"
    LOGOUT = "Log Out"
    LOGIN = "Log In"
    ERROR = "Okay"
    PROFILE = "My Profile"
    BACK = "Back"
    
def preset_button(
    type: DefaultButton,
    on_click: Callable[[ft.ElevatedButton], None] = lambda f: print(f"{DefaultButton.value} button pressed! {f.text}"),
    preset_icon: ft.IconValue = None,
    style: ft.ButtonStyle = default_action_button_style
) -> ft.ElevatedButton:
    if type == DefaultButton.LOGOUT:
        preset_icon = ft.Icons.LOGOUT
    elif type == DefaultButton.LOGIN:
        preset_icon = ft.Icons.LOGIN
    elif type == DefaultButton.ERROR:
        style = build_action_button_style(
            primary=ft.Colors.ERROR,
            on_primary=ft.Colors.ON_ERROR,
            highlight=ft.Colors.ERROR
        )
    elif type == DefaultButton.PROFILE:
        preset_icon = ft.Icons.PERSON
    elif type == DefaultButton.BACK:
        preset_icon = ft.Icons.KEYBOARD_RETURN
    
    return default_action_button(
        text=type.value,
        on_click=on_click,
        icon=preset_icon,
        style=style
    )
