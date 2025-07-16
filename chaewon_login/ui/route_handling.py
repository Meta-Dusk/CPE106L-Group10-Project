import re
import flet as ft

from chaewon_login.db.db_manager import init_database
from chaewon_login.ui.login_ui import main_login_ui
from chaewon_login.ui.retry_ui import check_mongo_connection
from chaewon_login.ui.components.buttons import profile_button, logout_button
from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.db.mongo import connect_to_mongo
from chaewon_login.auth.user import is_authenticated, yes_clicked, no_clicked
from chaewon_login.ui.route_data import RouteHandler, PageRoute
from chaewon_login.ui.components.dialogs import confirm_logout_dialog


def preset_logout_button(
    page: ft.Page,
    page_destination: str
) -> ft.ElevatedButton:
    def on_click(e):
        dialog = confirm_logout_dialog(
            page=page,
            yes_clicked=lambda e: yes_clicked(page, dialog, page_destination),
            no_clicked=lambda e: no_clicked(page, dialog)
        )

    return logout_button(on_click=on_click)

# Shared page renderer
def render_page(page: ft.Page, content: ft.Control | list[ft.Control]):
    if not isinstance(content, list):
        content = [content]
    container = ft.Container(
        content=ft.Column(
            controls=content,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        expand=True,
    )
    page.controls.append(container)

def logout(page: ft.Page):
    page.session.clear()
    page.go(PageRoute.LOGIN.value)

# Route logic
def handle_loading(page: ft.Page, _):
    collection = init_database(page)
    if collection is not None:
        page.go(PageRoute.LOGIN.value)
    else:
        page.go(PageRoute.RETRY.value)

def handle_login(page: ft.Page, _):
    if is_authenticated(page):
        page.go(PageRoute.DASHBOARD.value)
        return
    main_login_ui(page)

def handle_retry(page: ft.Page, _):
    check_mongo_connection(page)

def handle_not_found(page: ft.Page, _):
    error_msg = default_text(TextType.TITLE, "404 - Page not found")
    error_msg.color = ft.Colors.RED
    render_page(page, error_msg)

def handle_dashboard(page: ft.Page, _):
    logout_btn = preset_logout_button(page, PageRoute.LOGIN.value)
    profile_btn = profile_button(page)
    msg = default_text(TextType.TITLE, "This is the dashboard 😔🤚")
    render_page(page, [msg, profile_btn, logout_btn])

def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    accounts_collection = connect_to_mongo()
    user_doc = accounts_collection.find_one({"username": user_id}) if accounts_collection is not None else None

    if user_doc:
        title = default_text(TextType.TITLE, f"👤 {user_doc['username']}'s Profile")
        subtitle = default_text(TextType.SUBTITLE, "Welcome back!")
    else:
        title = default_text(TextType.TITLE, "User not found 😢")
        subtitle = default_text(TextType.SUBTITLE, f"User ID: {user_id}")

    logout_btn = preset_logout_button(page, PageRoute.LOGIN.value)
    render_page(page, [title, subtitle, logout_btn])

DYNAMIC_ROUTE_HANDLERS = [
    {
        "pattern": re.compile(r"^/profile/(?P<user_id>\w+)$"),
        "handler": handle_profile,
        "auth_required": True
    },
    # More routes...
]

def match_dynamic_route(route: str):
    for entry in DYNAMIC_ROUTE_HANDLERS:
        match = entry["pattern"].match(route)
        if match:
            return entry, match.groupdict()
    return None, {}

# Central route registry
ROUTE_HANDLERS = {
    PageRoute.LOADING.value: RouteHandler(PageRoute.LOADING.value, handle_loading),
    PageRoute.LOGIN.value: RouteHandler(PageRoute.LOGIN.value, handle_login),
    PageRoute.RETRY.value: RouteHandler(PageRoute.RETRY.value, handle_retry),
    PageRoute.DASHBOARD.value: RouteHandler(PageRoute.DASHBOARD.value, handle_dashboard, auth_required=True)
}
