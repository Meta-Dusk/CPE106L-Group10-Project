import flet as ft
from db.db_manager import init_database
from ui.login_ui import main_login_ui
from ui.retry_ui import check_mongo_connection

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    collection = init_database(page)
    if collection is not None:
        main_login_ui(page)
    else:
        check_mongo_connection(page)

ft.app(target=main)
