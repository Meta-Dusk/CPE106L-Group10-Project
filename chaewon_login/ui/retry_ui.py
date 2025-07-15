import flet as ft

from chaewon_login.db.mongo import connect_to_mongo
from chaewon_login.ui.login_ui import main_login_ui
from chaewon_login.assets.images import ImageData, default_image
from chaewon_login.db.db_manager import init_database, toggle_db
from chaewon_login.ui.components import (
    default_text,
    TextType,
    default_container,
    default_column,
    default_alert_dialog
)

def check_mongo_connection(page: ft.Page):
    collection = connect_to_mongo()

    if collection is None:
        page.controls.clear()
        current_image = default_image()
        sad_chaewon = ImageData.CHAEWON_SAD.value
        current_image.src = sad_chaewon.path
        current_image.tooltip = sad_chaewon.description

        warning_title = default_text(TextType.TITLE, "Failed to connect to MongoDB.")
        warning_title.color = ft.Colors.RED
        warning_desc = default_text(TextType.SUBTITLE, "Please ensure the MongoDB cluster is running...")

        def retry(e):
            # Show loading while retrying
            new_collection = init_database(page)
            if new_collection is not None:
                page.go("/login")
            else:
                page.go("/retry")  # show again if still fails

        def switch_db(e):
            toggle_db()
            conn = init_database(page)

            if conn:
                page.go("/login")
            else:
                dialog_content = default_text(TextType.TITLE, "Failed to connect to SQLite.")
                dialog_content.color = ft.Colors.RED
                dialog = default_alert_dialog(
                    title=default_text(TextType.TITLE, "Error"),
                    content=dialog_content,
                    on_dismiss=lambda e: page.update()
                )
                dialog.open = True
                page.update()


        retry_button = ft.ElevatedButton(text="Retry Connection", on_click=retry)
        switch_button = ft.ElevatedButton(text="Switch to SQLite", on_click=switch_db)

        retry_ui = default_column(controls=
            [
                current_image,
                warning_title,
                warning_desc,
                retry_button,
                switch_button
            ]
        )

        page.add(
            default_container(retry_ui)
        )
        page.update()
        return None

    return collection
