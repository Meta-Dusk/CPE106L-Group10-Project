import re
import flet as ft

from chaewon_login.db.db_manager import init_database
from chaewon_login.ui.login_ui import main_login_ui
from chaewon_login.ui.retry_ui import check_mongo_connection
from chaewon_login.ui.components.buttons import preset_button, DefaultButton
from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.db.db_manager import find_user
from chaewon_login.auth.user import is_authenticated, logout_yes, logout_no
from chaewon_login.ui.route_data import RouteHandler, PageRoute
from chaewon_login.ui.components.dialogs import confirm_logout_dialog
from chaewon_login.ui.components.containers import default_column, default_container, div


# Construct logout button from presets
def preset_logout_button(
    page: ft.Page,
    page_destination: str = PageRoute.LOGIN.value
) -> ft.ElevatedButton:
    def on_click(e):
        dialog = confirm_logout_dialog(
            page=page,
            yes_clicked=lambda e: logout_yes(page, dialog, page_destination),
            no_clicked=lambda e: logout_no(page, dialog)
        )

    return preset_button(DefaultButton.LOGOUT, on_click=on_click)

# Shared page renderer
def render_page(page: ft.Page, content: ft.Control | list[ft.Control]):
    if not isinstance(content, list):
        content = [content]
    form = default_column(content)
    container = default_container(form)
    page.controls.append(container)

# == Route logic ==
def handle_loading(page: ft.Page, _):
    def after_init():
        from chaewon_login.db.db_manager import get_collection
        collection = get_collection()

        if collection is not None:
            print("Time to log in! - Chae.Debug")
            page.go(PageRoute.LOGIN.value)
        else:
            print("Why no connection - Chae.Debug")
            page.go(PageRoute.RETRY.value)

    init_database(page, callback=after_init)

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
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")
    
    msg = default_text(TextType.TITLE, "This is the dashboard 😔🤚")
            
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile)
    buttons = ft.Row(
        controls=[profile_btn, logout_btn],
        alignment=ft.MainAxisAlignment.END
    )
    
    render_page(page, [
        msg,
        div(),
        buttons
    ])

def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)

    if user_doc:
        title = default_text(TextType.TITLE, f"👤 | {user_doc['username']}'s Profile")
        subtitle = default_text(TextType.SUBTITLE, "Welcome back!")
    else:
        title = default_text(TextType.TITLE, "User not found 😢")
        subtitle = default_text(TextType.SUBTITLE, f"User ID: {user_id}")
        
    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)
    buttons = ft.Row(
        controls=[logout_btn, back_btn],
        alignment=ft.MainAxisAlignment.END
    )
    
    render_page(page, [
        title,
        subtitle,
        div(),
        buttons
    ])

# == Dynamic route registry ==
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

# == Central route registry ==
ROUTE_HANDLERS = {
    PageRoute.LOADING.value: RouteHandler(PageRoute.LOADING.value, handle_loading),
    PageRoute.LOGIN.value: RouteHandler(PageRoute.LOGIN.value, handle_login),
    PageRoute.RETRY.value: RouteHandler(PageRoute.RETRY.value, handle_retry),
    PageRoute.DASHBOARD.value: RouteHandler(PageRoute.DASHBOARD.value, handle_dashboard, auth_required=True)
}
