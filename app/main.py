import flet as ft
import asyncio

from app.assets.images import set_logo, build_image, ImageData
from app.assets.audio_manager import setup_audio, audio
from app.ui.animations import (
    animate_slide_in, container_setup, animate_slide_out, prepare_for_slide_in, teeter_right,
    animate_fade_in, animate_fade_out, text_pand)
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
    brand_animate = container_setup(brand)
    brand.opacity = 0.0

    logo = set_logo()
    logo.tooltip = ""
    logo.visible = False
    logo_animate = container_setup(logo)
    
    text = ft.Text(
        value="Group 10",
        text_align=ft.TextAlign.CENTER,
        style=ft.TextStyle(size=50, letter_spacing=10, word_spacing=20, weight=ft.FontWeight.W_100),
        expand=True,
        scale=ft.Scale(scale=1.0),
        animate_scale=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT)
    )
    text_animate = ft.Container(
        content=text,
        animate_opacity=ft.Animation(duration=0),
        animate_offset=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_rotation=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        opacity=0.0,
        offset=ft.Offset(0, 0),
        rotate=0,
        alignment=ft.alignment.center,
        expand=True
    )

    splashes = [logo_animate, brand_animate, text_animate]
    
    splash_skip_text = ft.Text("Tap or press any key to skip...", italic=True, opacity=0.5, color=ft.Colors.SECONDARY)
    splash_filler_container = ft.Container(ft.Text(""), alignment=ft.alignment.center, expand=True, height=200)
    
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
        text_animate.animate_opacity = ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT)
        await animate_fade_in(text_animate, 2000)
        await text_pand(text, 2000)
        page.update()
        
        brand.visible = True
        await animate_fade_out(text_animate)
        await animate_fade_in(brand, 2000)
        page.update()
        
        await animate_fade_out(brand)
        text_animate.visible = False
        brand.visible = False
        logo.visible = True
        await toggle_theme(page)
        
        await asyncio.sleep(1)
        
        await animate_slide_out(logo_animate)
        await prepare_for_slide_in(logo_animate)
        
        await asyncio.sleep(1)
        
        await toggle_theme(page)
        await animate_slide_in(logo_animate)
        await teeter_right(logo_animate)
        
        await asyncio.sleep(1)
        
    success = await splash_animation()
    if not success:
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
