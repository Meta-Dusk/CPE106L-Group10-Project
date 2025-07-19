import re
import flet as ft

from chaewon_login.db.db_manager import init_database
from chaewon_login.ui.screens.login_ui import main_login_ui
from chaewon_login.ui.screens.retry_ui import check_mongo_connection
from chaewon_login.ui.screens.dashboard_ui import handle_dashboard
from chaewon_login.ui.screens.profile_ui import handle_profile
from chaewon_login.ui.screens.shared_ui import render_page
from chaewon_login.ui.screens.viewgraphs import handle_viewgraphs
from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.auth.user import is_authenticated
from chaewon_login.routing.route_data import RouteHandler, PageRoute


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

def handle_not_found(page: ft.Page, _):
    error_msg = default_text(TextType.TITLE, "404 - Page not found")
    error_msg.color = ft.Colors.RED
    render_page(page, error_msg)


# == ROUTE REGISTRIES ==

ROUTE_HANDLERS = {
    PageRoute.LOADING.value: RouteHandler(PageRoute.LOADING.value, handle_loading),
    PageRoute.LOGIN.value: RouteHandler(PageRoute.LOGIN.value, handle_login),
    PageRoute.RETRY.value: RouteHandler(PageRoute.RETRY.value, check_mongo_connection),
    PageRoute.DASHBOARD.value: RouteHandler(PageRoute.DASHBOARD.value, handle_dashboard, auth_required=True),
    PageRoute.GRAPHS.value: RouteHandler(PageRoute.GRAPHS.value, handle_viewgraphs, auth_required=True)
}

DYNAMIC_ROUTE_HANDLERS = [
    {
        "pattern": re.compile(r"^/profile/(?P<user_id>\w+)$"),
        "handler": handle_profile,
        "auth_required": True
    }
]

def match_dynamic_route(route: str):
    for entry in DYNAMIC_ROUTE_HANDLERS:
        match = entry["pattern"].match(route)
        if match:
            return entry, match.groupdict()
    return None, {}
