import re
import flet as ft

from app.db.db_manager import init_database
from app.ui.screens.login_ui import main_login_ui
from app.ui.screens.retry_ui import check_mongo_connection
from app.ui.screens.dashboard_ui import handle_dashboard
from app.ui.screens.profile_ui import handle_profile
from app.ui.screens.shared_ui import render_page
from app.ui.screens.viewgraphs import handle_viewgraphs
from app.ui.screens.booking import handle_booking
from app.ui.screens.api_key_ui import handle_api_key_entry
from app.ui.screens.operator_ui import handle_operator
from app.ui.components.text import default_text, DefaultTextStyle
from app.auth.user import is_authenticated
from app.routing.route_data import RouteHandler, PageRoute


def handle_loading(page: ft.Page, _):
    def after_init():
        from app.db.db_manager import get_collection
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
    error_msg = default_text(DefaultTextStyle.TITLE, "404 - Page not found")
    error_msg.color = ft.Colors.RED
    render_page(page, error_msg)


# == ROUTE REGISTRIES ==

ROUTE_HANDLERS = {
    PageRoute.LOADING.value: RouteHandler(PageRoute.LOADING.value, handle_loading),
    PageRoute.LOGIN.value: RouteHandler(PageRoute.LOGIN.value, handle_login),
    PageRoute.RETRY.value: RouteHandler(PageRoute.RETRY.value, check_mongo_connection),
    PageRoute.DASHBOARD.value: RouteHandler(PageRoute.DASHBOARD.value, handle_dashboard, auth_required=True),
    PageRoute.GRAPHS.value: RouteHandler(PageRoute.GRAPHS.value, handle_viewgraphs, auth_required=True),
    PageRoute.BOOKING.value: RouteHandler(PageRoute.BOOKING.value, handle_booking),
    PageRoute.API_KEY.value: RouteHandler(PageRoute.API_KEY.value, handle_api_key_entry)
}

# Use for pages that are designed to be unique per user.
DYNAMIC_ROUTE_HANDLERS = [
    {
        "pattern": re.compile(r"^/profile/(?P<user_id>\w+)$"),
        "handler": handle_profile,
        "auth_required": True
    },
    {
        "pattern": re.compile(r"^/profile/op/(?P<user_id>\w+)$"),
        "handler": handle_operator,
        "auth_required": True
    }
]

def match_dynamic_route(route: str):
    for entry in DYNAMIC_ROUTE_HANDLERS:
        match = entry["pattern"].match(route)
        if match:
            return entry, match.groupdict()
    return None, {}
