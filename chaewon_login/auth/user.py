import flet as ft

def is_authenticated(page: ft.Page) -> bool:
    return bool(page.session.get("user_authenticated"))
