"""
ATraS (Accessible Transportation Scheduler) - Application Launcher

This launcher provides a user-friendly interface for starting the ATraS application
in different launch_modes (native window, web browser, or setup launch_mode). It automatically
checks for and installs required dependencies before launching the main application.

Features:
- Automatic dependency checking and installation
- Multiple launch launch_modes (Native, Web, Setup)
- Multiple window launch_modes (Windowed, Full Screen, Borderless Full Screen)
- Error handling and user feedback
- Clean UI with radio button selection

Authors: CPE106L Group 10
Version: 0.2.0
Date: 2025
"""

import sys
import subprocess
import tkinter as tk
import os
import re

from tkinter import messagebox
from pathlib import Path

# === CONFIGURATION ===
REQUIREMENTS_FILE = Path(__file__).resolve().parent / "requirements.txt"

# === DEPENDENCY MANAGEMENT FUNCTIONS ===

def parse_requirements(filename: Path):
    """
    Parse module names from requirements.txt
    Returns:
        list: Module names (e.g., 'flet', 'bcrypt')
    """
    modules = []
    if not filename.exists():
        raise FileNotFoundError(f"{filename} not found.")
    
    with filename.open("r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r"^([a-zA-Z0-9_\-]+)", line)
            if match:
                modules.append(match.group(1))
    return modules

def check_required_modules(modules):
    missing = []
    for mod in modules:
        try:
            __import__(mod)
        except ImportError:
            print(f"❌ Missing: {mod}")
            missing.append(mod)
    return missing

def install_requirements_file():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
        return True
    except subprocess.CalledProcessError:
        return False

# === USER INTERFACE FUNCTIONS ===

def prompt_install_modules(modules):
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askyesno(
        "Missing Required Modules",
        "The following modules are missing:\n\n" +
        "\n".join(modules) +
        "\n\nWould you like to install them now?"
    )
    root.destroy()
    return response

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

# === MAIN DEPENDENCY CHECK AND INSTALLATION ===
try:
    required_modules = parse_requirements(REQUIREMENTS_FILE)
except FileNotFoundError as e:
    tk.Tk().withdraw()
    messagebox.showerror("Missing File", str(e))
    sys.exit(1)

missing = check_required_modules(required_modules)

if missing:
    if prompt_install_modules(missing):
        success = install_requirements_file()
        if not success:
            show_fatal_error(missing)
        else:
            messagebox.showinfo("Success", "All missing modules were installed successfully.")
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        show_fatal_error(missing)
else:
    print("\n✅ All required modules are installed.\n")

# == Flet App starts here ==
# Only import your actual app logic if no missing modules
import flet as ft

from app.setup_env import setup_env
from app.ui.styles import apply_launcher_page_config
from app.ui.components.containers import default_row, div
from app.ui.components.buttons import (
    preset_radio_group, DefaultButton, preset_button, LaunchMode,
    WindowMode, DEFAULT_WINDOW_CHOICES, DEFAULT_LAUNCH_CHOICES)
from app.ui.components.text import default_text, DefaultTextStyle
from app.utils import load_launcher_config, save_launcher_config


# === Setup environment ===
env = os.environ.copy()
env["PYTHONPATH"] = str(Path(__file__).parent.resolve())
main_script = Path(__file__).parent / "app" / "main.py"


def launch_main_script(launch_mode: LaunchMode, window_mode: WindowMode, page: ft.Page):
    # Close Flet window before running subprocess
    page.window.close()
    print(
f"""
== Chosen Modes ==
Application: {launch_mode}
Window: {window_mode}
"""
    )
    if launch_mode == LaunchMode.SETUP.value:
        setup_env()
        subprocess.run(["py", "-m", "app.setup"], check=True)
        return

    run_args = []

    if launch_mode == LaunchMode.WEB.value:
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

    selected_launch_mode = ft.Ref[ft.RadioGroup]()
    selected_window_mode = ft.Ref[ft.RadioGroup]()
    window_radio_refs = {}

    # Load saved config if exists
    config = load_launcher_config()
    initial_launch_mode = config.get("launch_mode")
    initial_window_mode = config.get("window_mode")
    
    def enforce_window_mode_constraints(selected_launch):
        invalid_modes = [WindowMode.FULLSCREEN.value, WindowMode.BORDERLESS.value]
        should_disable = selected_launch in [LaunchMode.WEB.value, LaunchMode.SETUP.value]

        for key in window_radio_refs:
            ref = window_radio_refs[key]
            if ref and ref.current:
                ref.current.disabled = should_disable and key in invalid_modes
                ref.current.update()

        # Auto-switch to fallback if invalid is selected
        if selected_window_mode.current.value in invalid_modes and should_disable:
            selected_window_mode.current.value = WindowMode.WINDOWED.value
            selected_window_mode.current.update()

    def handle_launch_change(e):
        enforce_window_mode_constraints(e.control.value)

    launch_modes = preset_radio_group(
        ref=selected_launch_mode,
        choices=DEFAULT_LAUNCH_CHOICES,
        selected_value=initial_launch_mode,
        on_change=handle_launch_change
    )
    
    window_modes = preset_radio_group(
        ref=selected_window_mode,
        choices=DEFAULT_WINDOW_CHOICES,
        radio_refs_map=window_radio_refs,
        selected_value=initial_window_mode
    )
    
    def delayed_init(e):
        enforce_window_mode_constraints(initial_launch_mode)
        # Optionally, remove the handler if only needed once
        page.on_resized = None

    page.on_resized = delayed_init
    
    def on_submit(e):
        launch_mode = selected_launch_mode.current.value
        window_mode = selected_window_mode.current.value

        # Save selected values to JSON
        save_launcher_config(launch_mode, window_mode)

        for control in [launch_btn, cancel_btn]:
            control.disabled = True
        page.update()
        launch_main_script(launch_mode, window_mode, page)

    def on_cancel(e):
        page.window.close()

    label = default_text(DefaultTextStyle.TITLE, "How would you like to run the app?")

    launch_btn = preset_button(DefaultButton.LAUNCH, on_click=on_submit)
    launch_btn.autofocus = True
    cancel_btn = preset_button(DefaultButton.CANCEL, on_click=on_cancel)

    buttons = default_row([launch_btn, cancel_btn])
    
    launch_column = ft.Column(
        controls=[
            default_text(DefaultTextStyle.SUBTITLE, "Launch Mode"),
            launch_modes
        ],
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    launch_container = ft.Container(
        content=launch_column,
        expand=True,
        padding=10,
        alignment=ft.alignment.center
    )
    
    window_column = ft.Column(
        controls=[
            default_text(DefaultTextStyle.SUBTITLE, "Window Mode"),
            window_modes
        ],
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    window_container = ft.Container(
        content=window_column,
        expand=True,
        padding=10,
        alignment=ft.alignment.center
    )
    
    launch_modes_row = ft.Row(
        controls=[
            launch_container,
            window_container
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    launch_modes_container = ft.Container(
        content=launch_modes_row,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        padding=20,
        border_radius=10
    )

    form_controls = [
        label,
        div(),
        launch_modes_container,
        buttons
    ]
    form = ft.Column(
        controls=form_controls,
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(form)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="app/assets")
