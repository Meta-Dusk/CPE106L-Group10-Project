import flet as ft
from db.db_manager import init_database, get_current_mode
from ui.login_ui import main_login_ui

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    if init_database():
        main_login_ui(page)
    else:
        page.add(ft.Text("Database connection failed."))
        
ft.app(target=main)
