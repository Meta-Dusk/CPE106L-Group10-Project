"""
ATraS (Accessible Transportation Scheduler) - Application Launcher

This launcher provides a user-friendly interface for starting the ATraS application
in different modes (native window, web browser, or setup mode). It automatically
checks for and installs required dependencies before launching the main application.

Features:
- Automatic dependency checking and installation
- Multiple launch modes (Native, Web, Setup)
- Error handling and user feedback
- Clean UI with radio button selection

Authors: CPE106L Group 10
Version: 1.0.0
Date: 2025
"""

import sys
import subprocess
import tkinter as tk
import os

from tkinter import messagebox


# === CONFIGURATION ===
# List of required Python modules for the application to function properly
REQUIRED_MODULES = ["flet", "pymongo", "bcrypt", "cryptography", "matplotlib", "requests"]

# === DEPENDENCY MANAGEMENT FUNCTIONS ===

def check_required_modules():
    """
    Check if all required modules are installed.
    
    Returns:
        list: A list of missing module names. Empty list if all modules are available.
    """
    missing = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing

def install_missing_modules(modules):
    """
    Install missing Python modules using pip.
    
    Args:
        modules (list): List of module names to install
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *modules])
        return True
    except subprocess.CalledProcessError:
        return False

# === USER INTERFACE FUNCTIONS ===

def prompt_install_modules(modules):
    """
    Show a GUI dialog asking user permission to install missing modules.
    
    Args:
        modules (list): List of missing module names
        
    Returns:
        bool: True if user agrees to install, False otherwise
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    response = messagebox.askyesno(
        "Missing Required Modules",
        "The following modules are missing:\n\n" +
        "\n".join(modules) +
        "\n\nWould you like to automatically install them now?"
    )

    root.destroy()
    return response

def show_fatal_error(modules):
    """
    Show an error dialog for failed installations and exit the application.
    
    Args:
        modules (list): List of modules that failed to install
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    
    messagebox.showerror(
        "Installation Failed",
        "The following modules could not be installed:\n\n" +
        "\n".join(modules) +
        "\n\nPlease install them manually."
    )
    root.destroy()
    sys.exit(1)

# === MAIN DEPENDENCY CHECK AND INSTALLATION ===
# Perform dependency check before importing application modules

missing = check_required_modules()

if missing:
    # Missing modules found - ask user for permission to install
    if prompt_install_modules(missing):
        success = install_missing_modules(missing)
        if not success:
            show_fatal_error(missing)
        else:
            messagebox.showinfo("Success", "All missing modules were installed successfully.")
            # Restart the script to ensure new modules are properly loaded
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        # User declined installation - show error and exit
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
