import flet as ft
import asyncio

from app.assets.images import set_logo, build_image, ImageData
from app.assets.audio_manager import setup_audio, audio
from app.ui.animations import (
    animate_slide_in, animate_slide_out, prepare_for_slide_in, teeter_right, animate_fade_in,
    animate_fade_out, text_pand, container_setup)
from app.ui.styles import apply_default_page_config
from app.ui.transitions import fade_in
from app.ui.components.containers import default_column
from app.ui.services.splash_service import SplashHandler
from app.routing.route_handling import ROUTE_HANDLERS, handle_not_found, match_dynamic_route
from app.routing.route_data import PageRoute
from app.auth.user import is_authenticated


LOGIN_PAGE = PageRoute.LOGIN.value


async def toggle_theme(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

async def run_splash_screen(page: ft.Page):
    handler = SplashHandler(page)
    page.on_keyboard_event = handler.on_skip_event
        
    brand = build_image(ImageData.METADUSK, relative_scale=1.2, visible=False)
    brand.tooltip = ""
    brand.opacity = 0.0

    logo = set_logo()
    logo.tooltip = ""
    logo_animate = container_setup(logo)
    logo_animate.visible = False
    
    text = ft.Text(
        value="Group 10",
        text_align=ft.TextAlign.CENTER,
        style=ft.TextStyle(size=50, letter_spacing=10, word_spacing=20, weight=ft.FontWeight.W_100),
        expand=True,
        visible=False
    )

    splashes = [logo_animate, brand, text]
    
    splash_skip_text = ft.Text("Tap or press any key to skip...", italic=True, opacity=0.5, color=ft.Colors.SECONDARY)
    splash_filler_container = ft.Container(ft.Text(""), alignment=ft.alignment.center, expand=True, height=170)
    
    splash_column = default_column([
        splash_skip_text,
        splash_filler_container,
        *splashes # Unpack splashes since you can't nest a list of controls in another list of controls
    ])

    splash_container = ft.Container(splash_column, alignment=ft.alignment.center, expand=True)
    
    page.add(splash_container)
    page.update()
    
    @handler.skippable_animation(auto_cleanup=True)
    async def splash_animation():
        await asyncio.sleep(0.5)
        text.visible = True
        await animate_fade_in(text, 1000)
        await text_pand(text, 1000)
        await animate_fade_out(text, 1000)
        text.visible = False
        brand.visible = True
        await animate_fade_in(brand, 1000)
        await animate_fade_out(brand, 1000)
        brand.visible = False
        logo_animate.visible = True
        await animate_fade_in(logo_animate, 1000)
        await toggle_theme(page)
        await asyncio.sleep(0.5)
        await animate_slide_out(logo_animate)
        await prepare_for_slide_in(logo_animate)
        await asyncio.sleep(0.5)
        await toggle_theme(page)
        await animate_slide_in(logo_animate)
        await teeter_right(logo_animate)
        await asyncio.sleep(1)
        
    success = await splash_animation()
    if not success:
        print("User has issued a command: Skip splash screen animations")
        return # Splash screen skipped


async def main(page: ft.Page):
    setup_audio()
    audio.on_ready(lambda: audio.play_random_bgm())
    apply_default_page_config(page)
    page.title = "ATraS (Accessible Transportation Scheduler)"
    await run_splash_screen(page)
    
    # --- Continue with App Setup ---

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()

        route = ROUTE_HANDLERS.get(page.route)
        if route:
            if route.auth_required and not is_authenticated(page):
                page.go(LOGIN_PAGE)
                return
            route.handler(page, e)
        else:
            dynamic, params = match_dynamic_route(page.route)
            if dynamic:
                if dynamic["auth_required"] and not is_authenticated(page):
                    page.go(LOGIN_PAGE)
                    return
                dynamic["handler"](page, e, **params)
            else:
                handle_not_found(page, e)

        fade_in(page)


    page.on_route_change = route_change
    page.go(page.route or LOGIN_PAGE)

ft.app(target=main, assets_dir="app/assets")
