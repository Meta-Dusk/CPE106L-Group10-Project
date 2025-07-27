import flet as ft

from app.assets.images import ImageData, build_image
from app.assets.audio_manager import audio, SFX
from app.ui.components.containers import default_container, default_column
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.dialogs import default_notif_dialog
from app.ui.components.buttons import default_action_button
from app.db.mongo import connect_to_mongo
from app.db.db_manager import init_database, toggle_db
from app.routing.route_data import PageRoute


login_page = PageRoute.LOGIN.value
retry_page = PageRoute.RETRY.value

def check_mongo_connection(page: ft.Page, _):
    collection = connect_to_mongo()

    if collection is None:
        audio.play_sfx(SFX.ERROR)
        page.controls.clear()
        current_image = build_image(ref=ImageData.CHAEWON_SAD, border_radius=75, set_size=200)

        warning_title = default_text(DefaultTextStyle.TITLE, "Failed to connect to MongoDB.")
        warning_title.color = ft.Colors.ERROR
        
        warning_desc = default_text(
            DefaultTextStyle.SUBTITLE,
            "Please ensure the MongoDB cluster is running or that you have finished setup first!"
        )
        
        error_dialog = default_notif_dialog(
            title="Failed to Reconnect",
            content=default_text(DefaultTextStyle.ERROR, "Have you tried running the setup again?")
        )

        def retry(e):
            new_collection = init_database()
            if new_collection is not None:
                page.go(login_page)
            else:
                audio.play_sfx(SFX.ERROR)
                page.go(retry_page)  # show again if still fails
                page.open(error_dialog)

        # def switch_db(e):
        #     toggle_db()
        #     conn = init_database(page)

        #     if conn:
        #         page.go(login_page)
        #     else:
        #         audio.play_sfx(SFX.ERROR)
        #         dialog_content = default_text(DefaultTextStyle.SUBTITLE, "Failed to connect to SQLite.")
        #         dialog_content.color = ft.Colors.ERROR
        #         dialog = default_notif_dialog(
        #             title=default_text(DefaultTextStyle.TITLE, "Error"),
        #             content=dialog_content,
        #             on_dismiss=lambda e: page.update()
        #         )
        #         page.open(dialog)
        #         page.update()

        retry_btn = default_action_button(text="Retry Connection", on_click=retry, width=300)
        # switch_btn = default_action_button(text="Switch to SQLite", on_click=switch_db, width=300)

        retry_ui = default_column([
            current_image,
            warning_title,
            warning_desc,
            retry_btn,
            # switch_btn
        ])

        page.add(default_container(retry_ui))
        page.update()
        return None

    return collection
