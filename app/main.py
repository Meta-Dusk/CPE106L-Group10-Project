import flet as ft
import asyncio

from app.assets.images import set_logo, build_image, ImageData
from app.assets.audio_manager import setup_audio, audio
from app.ui.animations import animate_slide_in, container_setup, animated_slide_out, prepare_for_slide_in, teeter_right
from app.ui.styles import apply_default_page_config
from app.ui.transitions import fade_in
from app.ui.components.containers import default_column
from app.routing.route_handling import ROUTE_HANDLERS, handle_not_found, match_dynamic_route
from app.routing.route_data import PageRoute
from app.auth.user import is_authenticated


LOGIN_PAGE = PageRoute.LOGIN.value


async def run_splash_screen(page: ft.Page):
    skip_event = asyncio.Event()
    skip_triggered = False

    def on_skip_event(e: ft.KeyboardEvent):
        nonlocal skip_triggered
        if not skip_triggered:
            print("User triggered skip!")
            skip_triggered = True
            skip_event.set()
            
    async def toggle_theme():
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
        
    def cleanup():
        page.controls.clear()
        page.on_keyboard_event = None
        page.update()
        
    async def await_or_skip(timeout: float) -> bool:
        try:
            await asyncio.wait_for(skip_event.wait(), timeout)
        except asyncio.TimeoutError:
            return False
        return True

    async def check_skip_and_cleanup(timeout: float) -> bool:
        if await await_or_skip(timeout):
            print("Skip was triggered. Skipping remaining splash animations.")
            cleanup()
            return True
        return False
        
    skip_event.clear()
        
    # Setup splash visuals (same as before)
    brand = build_image(ImageData.METADUSK, relative_scale=1.4)
    brand.offset = ft.Offset(0.0, -0.1)

    splash = set_logo()
    splash_animate = container_setup(splash)

    splashes = [splash_animate, brand]
    
    splash_column = default_column([
        ft.Text("Tap or press any key to skip...", italic=True, opacity=0.5, color=ft.Colors.SECONDARY),
        ft.Container(ft.Text(""), alignment=ft.alignment.center, expand=True, height=200),
        splashes
    ])

    splash_container = ft.Container(splash_column, alignment=ft.alignment.center, expand=True)

    splash.visible = False
    page.add(splash_container)
    page.on_keyboard_event = on_skip_event
    page.update()
    
    if await check_skip_and_cleanup(2): return
    
    brand.visible = False
    splash.visible = True
    await toggle_theme()
    
    if await check_skip_and_cleanup(1): return
    
    await animated_slide_out(splash_animate)
    await prepare_for_slide_in(splash_animate)
    
    if await check_skip_and_cleanup(1): return
    
    await toggle_theme()
    await animate_slide_in(splash_animate)
    await teeter_right(splash_animate)
    
    if await check_skip_and_cleanup(1): return


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
