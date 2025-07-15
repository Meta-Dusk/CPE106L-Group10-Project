import flet as ft

def fade_in(page: ft.Page, duration: int = 300):
    page.opacity = 0
    page.update()
    page.animate_opacity = duration
    page.opacity = 1
    page.update()
