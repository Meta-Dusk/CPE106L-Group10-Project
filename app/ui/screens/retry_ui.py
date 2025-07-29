import flet as ft

from app.assets.images import ImageData, set_logo
from app.assets.audio_manager import audio, SFX
from app.ui.components.containers import default_container, default_column, default_row, div
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.dialogs import default_notif_dialog
from app.ui.components.buttons import default_action_button, preset_button, DefaultButton
from app.db.mongo import connect_to_mongo
from app.db.db_manager import init_database, toggle_db, get_current_mode
from app.routing.route_data import PageRoute


login_page = PageRoute.LOGIN.value
retry_page = PageRoute.RETRY.value


def retry_ui(page: ft.Page):
    audio.play_sfx(SFX.ERROR)
    page.controls.clear()
    current_image = set_logo(ImageData.ICON_LIGHT)

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

    def switch_db(e):
        toggle_db()
        page.controls.clear()
        page.go(PageRoute.LOGIN.value)
        page.update()
    
    retry_btn = default_action_button(text="Retry Connection", on_click=retry)
    exit_btn = preset_button(DefaultButton.EXIT, on_click=lambda e: page.window.close())
    switch_db_btn = default_action_button(text="Switch to SQLite", on_click=switch_db)
    
    buttons = [retry_btn, exit_btn, switch_db_btn]
    buttons_row = default_row(buttons)
    
    text_column = default_column([warning_title, warning_desc])
    text_container = ft.Container(
        content=text_column,
        expand=True,
        padding=20,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        width=800,
        height=120,
        border_radius=30,
        adaptive=True
    )
    
    retry_ui = default_column([
        current_image,
        div(),
        text_container,
        buttons_row
    ])

    page.add(default_container(retry_ui))
    page.update()
    return None

def check_mongo_connection(page: ft.Page, _):
    collection = connect_to_mongo()

    if collection is None:
        retry_ui(page)

    return collection
