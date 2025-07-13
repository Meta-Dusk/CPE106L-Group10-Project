import flet as ft
from chaewon_login.db.mongo import connect_to_mongo
from chaewon_login.ui.login_ui import main_login_ui
from chaewon_login.assets.images import ImageData, default_image
from chaewon_login.constants import TEXT_LABEL_SIZE
from chaewon_login.db.db_manager import init_database, toggle_db

def check_mongo_connection(page: ft.Page):
    collection = connect_to_mongo()

    if collection is None:
        page.controls.clear()
        current_image = default_image()
        sad_chaewon = ImageData.CHAEWON_SAD.value
        current_image.src = sad_chaewon.url
        current_image.tooltip = sad_chaewon.description

        warning_title = ft.Text("Failed to connect to MongoDB.", color=ft.Colors.RED, size=TEXT_LABEL_SIZE)
        warning_desc = ft.Text(f"Please ensure the MongoDB cluster is running...")

        def retry(e):
            # Show loading while retrying
            new_collection = init_database(page)
            if new_collection is not None:
                main_login_ui(page, new_collection)
            else:
                check_mongo_connection(page)  # show again if still fails

        def switch_db(e):
            toggle_db()
            conn = init_database(page)

            if conn:
                main_login_ui(page)
            else:
                dialog_content = ft.Text(
                    "Failed to connect to SQLite.",
                    color=ft.Colors.RED,
                    text_align=ft.TextAlign.CENTER,
                    size=TEXT_LABEL_SIZE
                )
                dialog = ft.AlertDialog(
                    title=ft.Text("Error", text_align=ft.TextAlign.CENTER, size=TEXT_LABEL_SIZE, weight=ft.FontWeight.BOLD),
                    content=dialog_content,
                    alignment=ft.alignment.center,
                    on_dismiss=lambda e: page.update(),
                    title_padding=ft.padding.all(25),
                    adaptive=True,
                    icon=ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
                )
                dialog.open = True
                page.update()


        retry_button = ft.ElevatedButton(text="Retry Connection", on_click=retry)
        switch_button = ft.ElevatedButton(text="Switch to SQLite", on_click=switch_db)

        retry_ui = ft.Column(
            [
                current_image,
                warning_title,
                warning_desc,
                retry_button,
                switch_button
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
        page.update()
        return None

    return collection
