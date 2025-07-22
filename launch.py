import sys
import subprocess
import tkinter as tk
import os

from tkinter import messagebox


REQUIRED_MODULES = ["flet", "pymongo", "bcrypt", "cryptography", "matplotlib"]

def check_required_modules():
    missing = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing

# Function to install missing packages using pip
def install_missing_modules(modules):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *modules])
        return True
    except subprocess.CalledProcessError:
        return False

# GUI message using tkinter
def prompt_install_modules(modules):
    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno(
        "Missing Required Modules",
        "The following modules are missing:\n\n" +
        "\n".join(modules) +
        "\n\nWould you like to automatically install them now?"
    )

    root.destroy()
    return response

# Show fatal error and exit
def show_fatal_error(modules):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Installation Failed",
        "The following modules could not be installed:\n\n" +
        "\n".join(modules) +
        "\n\nPlease install them manually."
    )
    root.destroy()
    sys.exit(1)

# Main check before launching app
missing = check_required_modules()

if missing:
    if prompt_install_modules(missing):
        success = install_missing_modules(missing)
        if not success:
            show_fatal_error(missing)
        else:
            messagebox.showinfo("Success", "All missing modules were installed successfully.")
            # Optional: Restart the script automatically
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        show_fatal_error(missing)
else:
    print("\n✅ All required modules are installed.\n")

# == Flet App starts here ==
# Only import your actual app logic if no missing modules

import subprocess
import os
from pathlib import Path
import flet as ft

from app.setup_env import setup_env
from app.ui.styles import apply_launcher_page_config
from app.ui.components.containers import default_row, div
from app.ui.components.buttons import (launch_mode_radio_group, DefaultButton, preset_button, LaunchMode)
from app.ui.components.text import default_text, DefaultTextStyle


# === Setup environment ===
env = os.environ.copy()
env["PYTHONPATH"] = str(Path(__file__).parent.resolve())
main_script = Path(__file__).parent / "app" / "main.py"


def launch_main_script(mode: LaunchMode, page: ft.Page):
    # Close Flet window before running subprocess
    page.window.close()
    print(f"\nChosen mode: {mode}\n")
    if mode == LaunchMode.SETUP.value:
        setup_env()
        subprocess.run(["py", "-m", "app.setup"], check=True)
        return

    run_args = []

    if mode == LaunchMode.WEB.value:
        run_args.append("--web")

    run_args.append(str(main_script))

    try:
        subprocess.run(
            ["flet", "run", *run_args],
            check=True,
            env=env
        )
    except subprocess.CalledProcessError as e:
        subprocess.run([
            "py", "-c",
            (
                "import tkinter as tk; "
                "from tkinter import messagebox; "
                "root = tk.Tk(); root.withdraw(); "
                f"messagebox.showerror('Error', 'Flet app failed to run:\\n{str(e).replace(chr(39), chr(92) + chr(39))}')"
            )
        ])
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

    label = default_text(DefaultTextStyle.TITLE, "How would you like to run the app?")

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
    ft.app(target=main, assets_dir="app/assets")
