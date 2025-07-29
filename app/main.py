import flet as ft
import asyncio

from app.assets.images import set_logo, build_image, ImageData
from app.assets.audio_manager import setup_audio, audio
from app.ui.animations import (
    animate_slide_in, animate_slide_out, prepare_for_slide_in, teeter_right, animate_fade_in,
    animate_fade_out, animate_text_pand, container_setup, animate_zoom_in)
from app.ui.styles import apply_default_page_config
from app.ui.transitions import fade_in
from app.ui.services.splash_service import SplashHandler
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.map_view.render import cleanup_map_view
from app.routing.route_handling import handle_not_found, get_route_handler
from app.routing.route_data import PageRoute
from app.auth.user import is_authenticated


LOGIN_PAGE = PageRoute.LOGIN.value


# Some helper functions
def prow(controls: list[ft.Control]):
    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=100
    )

def pcolumn(controls: list[ft.Control]):
    return ft.Column(
        controls=controls,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def pbuild(controls: list[ft.Control]):
    pcontrols = pcolumn(controls)
    return ft.Container(pcontrols)

def preset_build(ref: ImageData):
    return build_image(
        ref=ref,
        set_size=200,
        tooltip="",
        border_radius=100
    )

async def toggle_theme(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()


async def run_splash_screen(page: ft.Page):
    handler = SplashHandler(page)
    page.on_keyboard_event = handler.on_skip_event
        
    brand = build_image(ImageData.METADUSK, tooltip="")
    brand_animate = container_setup(brand)
    brand_animate.opacity = 0.0
    brand_animate.visible = False

    logo = set_logo()
    logo_animate = container_setup(logo)
    logo_animate.visible = False
    logo_animate.offset = ft.Offset(0.0, 0.0)
    
    icon = set_logo(ImageData.ICON_LIGHT)
    icon_animate = container_setup(icon)
    icon_animate.visible = False
    
    andrei = preset_build(ImageData.ANDREI)
    nigel = preset_build(ImageData.NIGEL)
    seth = preset_build(ImageData.SETH)
    
    andrei_text = default_text(DefaultTextStyle.SUBTITLE, ImageData.ANDREI.value.description)
    nigel_text = default_text(DefaultTextStyle.SUBTITLE, ImageData.NIGEL.value.description)
    seth_text = default_text(DefaultTextStyle.SUBTITLE, ImageData.SETH.value.description)
    
    andrei_portrait = pbuild([andrei_text, andrei])
    nigel_portrait = pbuild([nigel_text, nigel])
    seth_portrait = pbuild([seth_text, seth])
    
    portraits = [andrei_portrait, nigel_portrait, seth_portrait]
    
    portrait_row = container_setup(prow(portraits))
    portrait_row.opacity = 0.0
    portrait_row.visible = False
    portrait_row.offset = ft.Offset(0.0, 0.0)
    
    text = ft.Text(
        value="Group 10",
        text_align=ft.TextAlign.CENTER,
        style=ft.TextStyle(size=50, letter_spacing=10, word_spacing=20, weight=ft.FontWeight.W_100),
        expand=True,
        visible=False,
        offset=ft.Offset(0.0, 0.2)
    )
    
    splashes = [logo_animate, brand_animate, text, icon_animate, portrait_row]
    
    splash_skip_text = ft.Text(
        "Tap or press any key to skip...",
        italic=True, opacity=0.5, color=ft.Colors.SECONDARY
    )
    splash_filler_container = ft.Container(ft.Text(""), height=170, padding=None)
    
    splash_stack = ft.Stack(
        controls=splashes,
        alignment=ft.alignment.center,
        fit=ft.StackFit.LOOSE
    )
    splash_column = ft.Column(
        [
            splash_skip_text,
            splash_filler_container,
            splash_stack
        ],
        tight=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    splash_container = ft.Container(splash_column, alignment=ft.alignment.center)
    
    page.add(splash_container)
    page.update()
    
    @handler.skippable_animation(auto_cleanup=True)
    async def splash_animation():
        await asyncio.sleep(0.5)
        icon_animate.visible = True
        await animate_zoom_in(icon_animate, 1000)
        await asyncio.sleep(0.5)
        await animate_fade_out(icon_animate, 1000)
        icon_animate.visible = False
        text.visible = True
        await animate_fade_in(text, 1000)
        await animate_text_pand(text, 1000)
        await animate_fade_out(text, 1000)
        text.visible = False
        portrait_row.visible = True
        await animate_fade_in(portrait_row, 1000)
        await asyncio.sleep(0.5)
        await animate_fade_out(portrait_row, 1000)
        portrait_row.visible = False
        brand_animate.visible = True
        await animate_fade_in(brand_animate, 1000)
        await asyncio.sleep(0.5)
        await animate_fade_out(brand_animate, 1000)
        brand_animate.visible = False
        logo_animate.visible = True
        await animate_fade_in(logo_animate, 500)
        await animate_slide_out(logo_animate)
        await toggle_theme(page)
        await prepare_for_slide_in(logo_animate)
        await asyncio.sleep(0.5)
        await animate_slide_in(logo_animate)
        await toggle_theme(page)
        await teeter_right(logo_animate)
        await asyncio.sleep(0.5)
        await animate_fade_out(logo_animate, 1000)
        
    success = await splash_animation()
    if not success:
        print("[Splash Screen] Skipping splash screen animations.")
        return


async def main(page: ft.Page):
    setup_audio()
    audio.on_ready(lambda: audio.play_random_bgm())
    apply_default_page_config(page)
    page.title = "ATraS (Accessible Transportation Scheduler)"
    await run_splash_screen(page)
    
    # --- Continue with App Setup ---

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()
        cleanup_map_view()

        route_handler, params = get_route_handler(page.route)

        if route_handler:
            if route_handler.auth_required and not is_authenticated(page):
                page.go(PageRoute.LOGIN.value)
                return
            route_handler.handler(page, e, **params)
        else:
            handle_not_found(page, e)

        asyncio.run(fade_in(page))


    page.on_route_change = route_change
    page.go(page.route or LOGIN_PAGE)

ft.app(target=main, assets_dir="app/assets")
