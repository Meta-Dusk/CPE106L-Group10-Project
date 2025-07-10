import flet as ft
from db.mongo import connect_to_mongo, MONGODB_CONNECTION_STRING
from ui.login_ui import main_login_ui
from assets.images import image_sources, default_image
from constants import text_label_size

def check_mongo_connection(page: ft.Page):
    collection = connect_to_mongo()

    if collection is None:
        sad_chaewon = default_image()
        sad_chaewon.src = image_sources["chaewon_sad"]

        warning_title = ft.Text("Failed to connect to MongoDB.", color=ft.Colors.RED, size=text_label_size)
        warning_desc = ft.Text(f"Please ensure MongoDB is running on {MONGODB_CONNECTION_STRING}.")

        def retry(e):
            page.controls.clear()
            page.update()
            new_collection = check_mongo_connection(page)
            if new_collection:
                main_login_ui(page, new_collection)

        retry_button = ft.ElevatedButton(text="Retry Connection", on_click=retry)

        retry_ui = ft.Column(
            [
                sad_chaewon,
                warning_title,
                warning_desc,
                retry_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )

        page.add(
            ft.Container(
                content=retry_ui,
                alignment=ft.alignment.center,
                expand=True,
            )
        )

        return None

    return collection
