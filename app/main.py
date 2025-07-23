import flet as ft
    
from app.ui.styles import apply_default_page_config
from app.routing.route_handling import (
    ROUTE_HANDLERS, handle_not_found, match_dynamic_route)
from app.routing.route_data import PageRoute
from app.ui.transitions import fade_in
from app.auth.user import is_authenticated


LOGIN_PAGE = PageRoute.LOGIN.value

def main(page: ft.Page):
    page.title = "ATraS (Accessible Transportation Scheduler)"
    apply_default_page_config(page)

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
