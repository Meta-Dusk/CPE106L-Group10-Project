import sys
import tkinter as tk

from tkinter import messagebox


# Check for required modules
def check_required_modules():
    required_modules = ["flet", "pymongo", "bcrypt", "cryptography"]
    missing = []
    for mod in required_modules:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing

# Show missing module alert with tkinter
def show_missing_modules_message(missing_modules):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Missing Required Modules",
        "The following modules are missing:\n\n" +
        "\n".join(missing_modules) +
        "\n\nPlease install them before running the application."
    )
    root.destroy()

# Run the check before importing anything else
missing = check_required_modules()
if missing:
    show_missing_modules_message(missing)
    sys.exit(1)

# == Flet App starts here ==
# Only import your actual app logic if no missing modules
import flet as ft

from chaewon_login.ui.styles import apply_default_page_config
from chaewon_login.ui.route_handling import (
    ROUTE_HANDLERS,
    handle_not_found,
    match_dynamic_route
)
from chaewon_login.ui.route_data import PageRoute
from chaewon_login.ui.transitions import fade_in
from chaewon_login.auth.user import is_authenticated


def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    apply_default_page_config(page)

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()

        route = ROUTE_HANDLERS.get(page.route)
        if route:
            if route.auth_required and not is_authenticated(page):
                page.go(PageRoute.LOGIN.value)
                return
            route.handler(page, e)
        else:
            dynamic, params = match_dynamic_route(page.route)
            if dynamic:
                if dynamic["auth_required"] and not is_authenticated(page):
                    page.go(PageRoute.LOGIN.value)
                    return
                dynamic["handler"](page, e, **params)
            else:
                handle_not_found(page, e)

        fade_in(page)


    page.on_route_change = route_change
    page.go(page.route or PageRoute.LOADING.value)

ft.app(target=main, assets_dir="chaewon_login/assets")
