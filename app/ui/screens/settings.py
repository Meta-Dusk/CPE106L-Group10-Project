import flet as ft

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import (
    div, default_row, spaced_buttons, preset_container, default_column)
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme, preset_exit_button)
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.assets.audio_manager import audio
from app.routing.route_helpers import open_profile
from app.utils import conv_percentage


def handle_settings(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "Settings")
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, theme_toggle],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
    
    def update_sfx(e):
        if audio.muted:
            value = audio.get_sfx_volume()
            sfx_volume_slider.disabled = True
        else:
            value = sfx_volume_slider.value
            sfx_volume_slider.disabled = False
        sfx_volume_slider.value = value
        sfx_volume_slider.label = f"SFX -> {conv_percentage(value)}"
        sfx_volume_slider.update()
        
    def update_bgm(e):
        if audio.muted:
            value = audio.get_bgm_volume()
            bgm_volume_slider.disabled = True
        else:
            value = bgm_volume_slider.value
            bgm_volume_slider.disabled = False
        bgm_volume_slider.value = value
        bgm_volume_slider.label = f"BGM -> {conv_percentage(value)}"
        bgm_volume_slider.update()
    
    def toggle_mute(e):
        if audio.muted:
            audio.unmute()
            audio._muted = False
        else:
            audio._muted = True
            audio.mute()
        update_sfx(e)
        update_bgm(e)
    
    def on_sfx_volume_change(e):
        update_sfx(e)
        audio.set_sfx_volume(sfx_volume_slider.value)
    
    def on_bgm_volume_change(e):
        update_bgm(e)
        audio.set_bgm_volume(bgm_volume_slider.value)
    
        
    mute_button = default_action_button(
        text="Mute Sounds",
        tooltip="Mutes all sounds",
        on_click=toggle_mute,
        icon=ft.Icons.VOLUME_MUTE,
        icon_color=ft.Colors.PRIMARY
    )
    pause_button = default_action_button(
        text="Pause Sounds",
        tooltip="Pauses all sounds",
        on_click=lambda e: audio.pause(),
        icon=ft.Icons.PAUSE,
        icon_color=ft.Colors.PRIMARY
    )
    sfx_volume_title = default_text(DefaultTextStyle.SUBTITLE, "Set SFX Volume")
    sfx_volume_slider = ft.Slider(
        min=0.0,
        max=1.0,
        divisions=10,
        value=audio.get_sfx_volume(),
        label=f"SFX -> {conv_percentage(audio.get_sfx_volume())}",
        on_change=on_sfx_volume_change
    )
    
    bgm_volume_title = default_text(DefaultTextStyle.SUBTITLE, "Set BGM Volume")
    bgm_volume_slider = ft.Slider(
        min=0.0,
        max=1.0,
        divisions=10,
        value=audio.get_bgm_volume(),
        label=f"BGM -> {conv_percentage(audio.get_bgm_volume())}",
        on_change=on_bgm_volume_change
    )
    
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    logout_btn = preset_logout_button(page)
    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=open_profile(page)
    )
    exit_btn = preset_exit_button(page)
    
    control_buttons = default_row([logout_btn, back_btn])
    top_row = spaced_buttons([exit_btn], [theme_toggle])
    title_container = preset_container(title, ft.Colors.PRIMARY_CONTAINER)
    
    sfx_volume_column = preset_container(default_column([sfx_volume_title, sfx_volume_slider]), ft.Colors.PRIMARY_CONTAINER)
    bgm_volume_column = preset_container(default_column([bgm_volume_title, bgm_volume_slider]), ft.Colors.PRIMARY_CONTAINER)
    volume_settings = default_row([sfx_volume_column, bgm_volume_column])
    
    settings_buttons = default_row([mute_button, pause_button])
    settings_column = default_column([volume_settings, settings_buttons])
    settings_container = preset_container(settings_column, ft.Colors.INVERSE_PRIMARY)
    
    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title_container,
        div(),
        settings_container,
        div(),
        control_buttons
    ])