import flet as ft
import asyncio

from app.assets.images import ImageData, build_image
from app.assets.audio_manager import audio, SFX
from app.auth.user import logout_yes, logout_no
from app.routing.route_data import PageRoute
from app.ui.components.dialogs import confirm_logout_dialog
from app.ui.components.buttons import preset_button, DefaultButton, reactive_text_button
from app.ui.components.containers import default_container
from app.ui.animations import animate_slide_in, animate_slide_out, prepare_for_slide_in, teeter_right
from app.ui.theme_service import save_theme_mode
from typing import Callable, Optional
from app.utils import enable_control_after_delay, get_loop, flatten_controls


def render_page(page: ft.Page, content: ft.Control):
    container = default_container(content)
    page.add(container)

def preset_logout_button(
    page: ft.Page, page_destination: str = PageRoute.LOGIN.value
) -> ft.ElevatedButton:
    def on_click(e):
        dialog = confirm_logout_dialog(
            page=page,
            yes_clicked=lambda e: logout_yes(page, dialog, page_destination),
            no_clicked=lambda e: logout_no(page, dialog)
        )
    return preset_button(DefaultButton.LOGOUT, on_click=on_click, on_click_sfx=SFX.ALERT)

def open_profile(page: ft.Page):
    def handler(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")
    return handler

def open_op(page: ft.Page):
    def handler(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/op/{user_id}")
    return handler

async def logo_toggle(
    page: ft.Page, toggleable_logo: ft.Control,
    current_image: ft.Image,
    first_image: ft.Image, second_image: ft.Image,
    e=None
):
    await animate_slide_out(toggleable_logo)
    await prepare_for_slide_in(toggleable_logo)

    # Toggle the image
    if current_image.src == first_image.src:
        current_image.src = second_image.src
        current_image.tooltip = second_image.tooltip
    else:
        current_image.src = first_image.src
        current_image.tooltip = first_image.tooltip

    toggleable_logo.content = current_image
    page.update()

    await animate_slide_in(toggleable_logo)
    await teeter_right(toggleable_logo)
    # await animate_reset(toggleable_logo)

async def toggle_theme(
    page: ft.Page, theme_toggle: ft.IconButton, toggleable_logo: ft.Control,
    current_image: ft.Image,
    first_image: ft.Image = build_image(ImageData.LOGO_LIGHT),
    second_image: ft.Image = build_image(ImageData.LOGO_DARK),
    e=None
):
    async def toggle(e):
        await asyncio.sleep(0.5)
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.Icons.DARK_MODE
        save_theme_mode(page.theme_mode)
        page.update()
            
    asyncio.create_task(logo_toggle(page, toggleable_logo, current_image, first_image, second_image, e))
    asyncio.create_task(toggle(e))
    

def theme_toggle_button(
    on_click: Callable[[ft.ElevatedButton], None] = None,
    on_click_sfx: Optional[SFX] = SFX.THEME
):
    def wrapped_on_click(e: ft.ControlEvent):
        audio.play_sfx(on_click_sfx)
        
        if on_click:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(on_click(e))
            except RuntimeError:
                asyncio.run_coroutine_threadsafe(on_click(e), get_loop())
    
    return ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Toggle Theme",
        on_click=wrapped_on_click,
    )
    
async def mod_toggle_theme(
    e, page: ft.Page, delay: float = 1.5,
    toggle_controls: ft.Control | list[ft.Control] = [],
    toggleable_logo: ft.Container = None,
    theme_toggle: ft.IconButton = None,
    logo: ft.Image = None
):
    # Flatten all controls
    compiled_controls = flatten_controls(toggle_controls)
        
    for control in compiled_controls:
        asyncio.create_task(enable_control_after_delay(control, delay))

    # Then perform the theme toggle
    await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
    
class StatusMessage:
    def __init__(self, text_control: ft.Text):
        self.text_control = text_control

    def show(self, message: str, color: str):
        self.text_control.value = message
        self.text_control.color = color
        self.text_control.update()

    def success(self, message: str):
        audio.play_sfx(SFX.REWARD)
        self.show(message, ft.Colors.TERTIARY)

    def error(self, message: str):
        audio.play_sfx(SFX.ERROR)
        self.show(message, ft.Colors.ERROR)

    def info(self, message: str):
        audio.play_sfx(SFX.NOTIF)
        self.show(message, ft.Colors.ON_SECONDARY_CONTAINER)

def preset_exit_button(page: ft.Page) -> ft.TextButton:
    return reactive_text_button(
        on_click=lambda e: page.window.close(),
        on_click_sfx=SFX.EXIT,
        on_click_text="Exiting...",
        on_focus_text=">Exit?<",
        on_hover_text="Exit?",
        text="Exit",
        width=80
    )