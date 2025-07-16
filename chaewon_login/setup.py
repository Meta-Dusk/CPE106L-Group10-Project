import flet as ft
import shutil

from chaewon_login.config import Config
from cryptography.fernet import Fernet
from chaewon_login.setup_env import setup_env
from chaewon_login.ui.styles import apply_default_page_config
from chaewon_login.ui.components.containers import default_container, default_row
from chaewon_login.ui.components.text import (
    default_text,
    TextType,
    default_input_field,
    InputFieldType
)
from chaewon_login.ui.components.buttons import default_action_button, cancel_button
from chaewon_login.ui.components.dialogs import default_alert_dialog


def ensure_directories():
    for path in [Config.KEY_PATH, Config.ENC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def generate_key():
    key = Fernet.generate_key()
    Config.KEY_PATH.write_bytes(key)
    return key


def encrypt_uri(key: bytes, uri: str):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(uri.encode())
    Config.ENC_PATH.write_bytes(encrypted)


def delete_directories():
    try:
        shutil.rmtree(Config.KEY_PATH.parent)
        shutil.rmtree(Config.ENC_PATH.parent)
        return True
    except Exception as e:
        return f"Failed to delete directories:\n{e}"


def handle_setup(page: ft.Page, entry: ft.TextField):
    uri = entry.value.strip()

    if not uri:
        page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("MongoDB URI cannot be empty."))
        page.dialog.open = True
        page.update()
        return

    setup_env()

    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        def reset_confirmed(e):
            dlg.open = False
            error = delete_directories()
            if error:
                page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(error))
                page.dialog.open = True
            else:
                perform_encryption(page, uri)
            page.update()

        def reset_canceled(e):
            dlg.open = False
            page.dialog = ft.AlertDialog(
                title=ft.Text("Setup Canceled"),
                content=ft.Text("Setup canceled. No changes were made.")
            )
            page.dialog.open = True
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Setup Already Exists"),
            content=ft.Text("A previous setup already exists.\nDo you want to reset it?"),
            actions=[
                ft.TextButton("Cancel", on_click=reset_canceled),
                ft.TextButton("Reset", on_click=reset_confirmed)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        page.dialog.open = True
        page.update()
        return

    perform_encryption(page, uri)


def perform_encryption(page: ft.Page, uri: str):
    ensure_directories()
    key = generate_key()
    encrypt_uri(key, uri)

    dlg = default_alert_dialog(
        icon=ft.Icon(name=ft.Icons.NOTIFICATIONS, color=ft.Colors.BLUE),
        title=ft.Text("Setup Complete"),
        content=ft.Text("MongoDB credentials have been encrypted and saved successfully.")
    )
    dlg = ft.AlertDialog(
        title=ft.Text("Setup Complete"),
        content=ft.Text("MongoDB credentials have been encrypted and saved successfully."),
        actions=[ft.TextButton("Close", on_click=lambda e: page.window_close())],
    )
    page.dialog = dlg
    page.dialog.open = True
    page.update()


def main(page: ft.Page):
    page.title = "Chaewon Setup"
    apply_default_page_config(page)

    label = default_text(TextType.TITLE, "MongoDB URI Setup")
    sublabel = default_text(TextType.SUBTITLE, "Enter your MongoDB URI:")

    entry = default_input_field(InputFieldType.PASSWORD, width=400)

    save_btn = default_action_button(
        "Save & Encrypt",
        on_click=lambda e: handle_setup(page, entry),
        bg_color=ft.Colors.GREEN
    )

    cancel_btn = cancel_button(on_click=lambda e: page.window.close())

    button_row = default_row([
        save_btn,
        cancel_btn
    ])

    content = default_container([label, sublabel, entry, button_row])
    page.add(content)


if __name__ == "__main__":
    ft.app(target=main)
