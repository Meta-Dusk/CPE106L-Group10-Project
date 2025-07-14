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

# Only import your actual app logic if no missing modules
import flet as ft
from db.db_manager import init_database
from ui.login_ui import main_login_ui
from ui.retry_ui import check_mongo_connection

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    collection = init_database(page)
    if collection is not None:
        main_login_ui(page)
    else:
        check_mongo_connection(page)

ft.app(target=main)
