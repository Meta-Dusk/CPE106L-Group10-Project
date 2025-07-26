import flet as ft
import inspect
import asyncio

from app.ui.components.containers import default_column
from typing import Callable, Optional
from app.assets.audio_manager import audio, SFX
from app.ui.styles import default_action_button_style, RadioChoiceStyle, WindowMode
from app.utils import log_button_press, run_async_in_thread
from enum import Enum
from functools import partial
from dataclasses import dataclass


# == Radio Button Group ==
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
    on_change: Optional[Callable] = None,
    on_change_sfx: Optional[SFX] = SFX.CLICK
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

    def wrapped_on_change(e: ft.ControlEvent):
        audio.play_sfx(on_change_sfx)
        result = on_change(e)
        if inspect.iscoroutine(result):
            run_async_in_thread(result)
    
    return ft.RadioGroup(
        ref=ref,
        value=selected,
        on_change=wrapped_on_change,
        content=default_column(controls=radios)
    )


# == Default Buttons ==    
def default_action_button(
    text: Optional[str] = "Action Button",
    on_click: Callable[[ft.ElevatedButton], None] = None,
    style: ft.ButtonStyle = default_action_button_style,
    icon: ft.IconValue = None,
    icon_color: ft.ColorValue = None,
    width: ft.OptionalNumber = 120,
    height: ft.OptionalNumber = 40,
    auto_focus: bool = False,
    tooltip: str = None,
    on_click_sfx: Optional[SFX] = SFX.CLICK,
    disabled: bool = False,
    visible: bool = True
) -> ft.ElevatedButton:
    if on_click is None:
        on_click = partial(log_button_press, text)
        
    def wrapped_on_click(e: ft.ControlEvent):
        audio.play_sfx(on_click_sfx)
        result = on_click(e)
        if inspect.iscoroutine(result):
            run_async_in_thread(result)
    
    button = ft.ElevatedButton(
        text=text,
        on_click=wrapped_on_click,
        width=width,
        height=height,
        style=style,
        expand=2,
        autofocus=auto_focus,
        tooltip=tooltip,
        icon=icon,
        icon_color=icon_color,
        disabled=disabled,
        visible=visible
    )
    return button

def default_text_button(
    text: Optional[str] = "Text Button",
    on_click: Callable[[ft.TextButton], None] = None,
    on_click_sfx: Optional[SFX] = SFX.CLICK,
    style: ft.ButtonStyle = None,
    icon: ft.IconValue = None,
    icon_color: ft.ColorValue = None,
    width: ft.OptionalNumber = None,
    height: ft.OptionalNumber = 40,
    auto_focus: bool = False,
    tooltip: str = None,
    disabled: bool = False
) -> ft.TextButton:
    if on_click is None:
        on_click = partial(log_button_press, text)
        
    def wrapped_on_click(e: ft.ControlEvent):
        audio.play_sfx(on_click_sfx)
        result = on_click(e)
        if inspect.iscoroutine(result):
            run_async_in_thread(result)
    
    button = ft.TextButton(
        text=text,
        on_click=wrapped_on_click,
        style=style,
        icon=icon,
        icon_color=icon_color,
        width=width,
        height=height,
        autofocus=auto_focus,
        tooltip=tooltip,
        expand=2,
        disabled=disabled,
        adaptive=True
    )
    return button


# == Preset Buttons ==
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
    on_click_sfx: Optional[SFX] = SFX.CLICK
) -> ft.ElevatedButton:
    data = type.value
    
    if on_click is None:
        on_click = partial(log_button_press, data.label)
    if type == DefaultButton.EXIT:
        width = 80
        on_click_sfx = SFX.BACK
    else:
        width = None
    
    def wrapped_on_click(e: ft.ControlEvent):
        audio.play_sfx(on_click_sfx)
        result = on_click(e)
        if inspect.iscoroutine(result):
            run_async_in_thread(result)
    
    return default_action_button(
        text=data.label,
        tooltip=data.tooltip,
        icon=data.icon,
        on_click=wrapped_on_click,
        style=style,
        auto_focus=auto_focus,
        width=width
    )

# == Reactive Buttons ==
def reactive_text_button(
    text: Optional[str] = "Reactive Text Button",
    on_click: Callable[[ft.ElevatedButton], None] = None,
    on_click_sfx: Optional[SFX] = SFX.CLICK,
    on_click_text: Optional[str] = "Click",
    on_hover_text: Optional[str] = "Hover",
    on_focus_text: Optional[str] = "Focus",
    style: ft.ButtonStyle = None,
    icon: ft.IconValue = None,
    icon_color: ft.ColorValue = None,
    width: ft.OptionalNumber = None,
    height: ft.OptionalNumber = 40,
    auto_focus: bool = False,
    tooltip: str = None,
    disabled: bool = False
) -> ft.TextButton:
    text_button = default_text_button(
        text=text,
        style=style,
        icon=icon,
        icon_color=icon_color,
        width=width,
        height=height,
        auto_focus=auto_focus,
        tooltip=tooltip,
        disabled=disabled
    )
    def update(e):
        if text_button.page:
            text_button.update()
        e.page.update()

    def on_hover(e: ft.HoverEvent):
        text_button.text = on_hover_text if e.data == "true" else text
        update(e)

    def on_focus(e: ft.OnFocusEvent):
        text_button.text = on_focus_text
        update(e)

    def on_blur(e):
        text_button.text = text
        update(e)
    
    def wrapped_on_click(e: ft.ControlEvent):
        text_button.text = on_click_text
        update(e)
        audio.play_sfx(on_click_sfx)
        
        result = on_click(e)
        if inspect.iscoroutine(result):
            run_async_in_thread(result)

    # Attach handlers after creation
    text_button.on_click = wrapped_on_click
    text_button.on_hover = on_hover
    text_button.on_focus = on_focus
    text_button.on_blur = on_blur

    return text_button