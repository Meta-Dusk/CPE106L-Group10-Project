import flet as ft

from app.routing.route_data import PageRoute

def build_route(template: str, **kwargs):
    """
    Converts a dynamic route template to a real route string.
    Example: "/profile/:user_id" with user_id="123" => "/profile/123"
    """
    route = template
    for key, value in kwargs.items():
        route = route.replace(f":{key}", str(value))
    return route

def open_profile(page: ft.Page):
    def handler(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(build_route(PageRoute.PROFILE.value, user_id=user_id))
    return handler

def open_op(page: ft.Page):
    def handler(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(build_route(PageRoute.OPERATOR.value, user_id=user_id))
    return handler
