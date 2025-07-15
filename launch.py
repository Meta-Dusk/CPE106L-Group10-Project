import subprocess
import os
import sys
from pathlib import Path
import flet as ft

from chaewon_login.setup_env import setup_env
from chaewon_login.ui.styles import apply_default_page_config
from chaewon_login.ui.components.containers import (default_column, default_row)
from chaewon_login.ui.components.buttons import (
    launch_button,
    cancel_button,
    launch_mode_radio_group
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
    page.title = "Chaewon App Launcher"
    apply_default_page_config(page)

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

    launch_btn = launch_button(on_click=on_submit)
    cancel_btn = cancel_button(on_click=on_cancel)

    buttons = default_row([launch_btn, cancel_btn])
    buttons = ft.Row(
        controls=[
            launch_btn,
            cancel_btn
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.add(
        # default_column([label, launch_modes, buttons])
        ft.Column(
            controls=([
                label,
                ft.Divider(),
                launch_modes,
                buttons
            ]),
            spacing=50,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
