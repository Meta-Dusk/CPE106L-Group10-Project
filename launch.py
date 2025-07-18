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
else:
    print("No missing modules. Starting launcher now...")

# == Flet App starts here ==
# Only import your actual app logic if no missing modules

import subprocess
import os
from pathlib import Path
import flet as ft

from chaewon_login.setup_env import setup_env
from chaewon_login.ui.styles import apply_launcher_page_config
from chaewon_login.ui.components.containers import default_row, div
from chaewon_login.ui.components.buttons import (
    launch_mode_radio_group,
    DefaultButton,
    preset_button
)
from chaewon_login.ui.components.text import default_text, TextType


# === Setup environment ===
env = os.environ.copy()
env["PYTHONPATH"] = str(Path(__file__).parent.resolve())
main_script = Path(__file__).parent / "chaewon_login" / "main.py"


def launch_main_script(mode: str, page: ft.Page):
    # Close Flet window before running subprocess
    page.window.close()

    if mode == "setup":
        setup_env()
        subprocess.run(["python", "-m", "chaewon_login.setup"], check=True)
        return

    mode_args = ["--web"] if mode == "web" else []

    try:
        subprocess.run(["flet", "run", *mode_args, str(main_script)], check=True, env=env)
    except subprocess.CalledProcessError as e:
        subprocess.run(["python", "-m", "tkinter", "-c",
                        f"from tkinter import messagebox; messagebox.showerror('Error', 'Flet app failed to run:\\n{e}')"])
        sys.exit(1)


def main(page: ft.Page):
    apply_launcher_page_config(page)

    selected_mode = ft.Ref[ft.RadioGroup]()

    def on_submit(e):
        selected = selected_mode.current.value
        for control in [launch_btn, cancel_btn]:
            control.disabled = True
        page.update()
        launch_main_script(selected, page)

    def on_cancel(e):
        page.window.close()

    label = default_text(TextType.TITLE, "How would you like to run the app?")

    launch_modes = launch_mode_radio_group(ref=selected_mode)

    launch_btn = preset_button(DefaultButton.LAUNCH, on_click=on_submit)
    launch_btn.autofocus = True
    cancel_btn = preset_button(DefaultButton.CANCEL, on_click=on_cancel)

    buttons = default_row([launch_btn, cancel_btn])

    form = ft.Column(
        controls=([
            label,
            div(),
            launch_modes,
            buttons
        ]),
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START
    )
    page.add(form)


if __name__ == "__main__":
    ft.app(target=main)
