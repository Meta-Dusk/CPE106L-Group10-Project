import flet as ft

from app.db.mongo import connect_to_mongo
from app.assets.images import ImageData, default_image
from app.db.db_manager import init_database, toggle_db
from app.ui.components.containers import default_container, default_column
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.dialogs import default_notif_dialog
from app.routing.route_data import PageRoute
from app.ui.components.buttons import default_action_button


login_page = PageRoute.LOGIN.value
retry_page = PageRoute.RETRY.value

def check_mongo_connection(page: ft.Page):
    collection = connect_to_mongo()

    if collection is None:
        page.controls.clear()
        current_image = default_image()
        sad_chaewon = ImageData.CHAEWON_SAD.value
        current_image.src = sad_chaewon.path
        current_image.tooltip = sad_chaewon.description

        warning_title = default_text(DefaultTextStyle.TITLE, "Failed to connect to MongoDB.")
        warning_title.color = ft.Colors.RED
        warning_desc = default_text(DefaultTextStyle.SUBTITLE, "Please ensure the MongoDB cluster is running...")

        def retry(e):
            # Show loading while retrying
            new_collection = init_database(page)
            if new_collection is not None:
                page.go(login_page)
            else:
                page.go(retry_page)  # show again if still fails

        def switch_db(e):
            toggle_db()
            conn = init_database(page)

            if conn:
                page.go(login_page)
            else:
                dialog_content = default_text(DefaultTextStyle.SUBTITLE, "Failed to connect to SQLite.")
                dialog_content.color = ft.Colors.RED
                dialog = default_notif_dialog(
                    title=default_text(DefaultTextStyle.TITLE, "Error"),
                    content=dialog_content,
                    on_dismiss=lambda e: page.update()
                )
                page.open(dialog)
                page.update()

        retry_btn = default_action_button(text="Retry Connection", on_click=retry)
        switch_btn = default_action_button(text="Switch to SQLite", on_click=switch_db)

        retry_ui = default_column(controls=
            [
                current_image,
                warning_title,
                warning_desc,
                retry_btn,
                switch_btn
            ]
        )

        page.add(
            default_container(retry_ui)
        )
        page.update()
        return None

    return collection
