import sys
import tkinter as tk

from tkinter import messagebox
from chaewon_login.ui.styles import apply_default_page_config

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

from chaewon_login.db.db_manager import init_database
from chaewon_login.ui.login_ui import main_login_ui
from chaewon_login.ui.retry_ui import check_mongo_connection
from chaewon_login.ui.components import (
    default_text,
    TextType,
    default_container,
    PageRoute
)

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    apply_default_page_config(page)

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()

        if page.route == PageRoute.LOADING.value:
            # import threading
            # def check_connection():
            #     collection = init_database(page)
            #     if collection is not None:
            #         page.go("/login")
            #     else:
            #         page.go("/retry")

            # threading.Thread(target=check_connection).start()
            collection = init_database(page)
            if collection is not None:
                page.go(PageRoute.LOGIN.value)
            else:
                page.go(PageRoute.RETRY.value)

        elif page.route == PageRoute.LOGIN.value:
            main_login_ui(page)

        elif page.route == PageRoute.RETRY.value:
            check_mongo_connection(page)

        else:
            error_msg = default_text(TextType.TITLE, "404 - Page not found")
            error_msg.color = ft.Colors.RED
            page.add(default_container(error_msg))

        page.update()

    page.on_route_change = route_change
    page.go(page.route or PageRoute.LOADING.value)

ft.app(target=main, assets_dir="chaewon_login/assets")
