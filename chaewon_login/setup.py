import flet as ft
import shutil
import asyncio

from chaewon_login.config import Config
from cryptography.fernet import Fernet
from chaewon_login.setup_env import setup_env
from chaewon_login.ui.styles import apply_setup_page_config
from chaewon_login.ui.components.containers import default_container, default_row
from chaewon_login.ui.components.text import default_text, TextType, uri_input_field
from chaewon_login.ui.components.buttons import default_action_button, preset_button, DefaultButton
from chaewon_login.ui.components.dialogs import default_alert_dialog, show_auto_closing_dialog
from pymongo.uri_parser import parse_uri


def validate_mongo_uri(uri: str) -> bool:
    try:
        parse_uri(uri)
        return True
    except Exception:
        return False

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


error_label = default_text(TextType.ERROR, "")

def handle_setup(page: ft.Page, entry: ft.TextField):
    uri = entry.value.strip()

    # Clear previous error
    error_label.visible = False
    error_label.value = ""
    page.update()

    if not uri:
        error_label.value = "MongoDB URI cannot be empty."
        error_label.visible = True
        page.update()
        return

    if not validate_mongo_uri(uri):
        error_label.value = "Invalid MongoDB URI format. Please double-check."
        error_label.visible = True
        page.update()
        return

    setup_env()

    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        def reset_confirmed(e):
            page.close(dialog)
            error_check = delete_directories()
            if not error_check:
                error_label.value = error_check
                error_label.visible = True
            else:
                perform_encryption(page, uri)
            page.update()

        def reset_canceled(e):
            page.close(dialog)
            canceled_dialog = ft.AlertDialog(
                title=ft.Text("Setup Canceled"),
                content=ft.Text("Setup canceled. No changes were made.")
            )
            page.open(canceled_dialog)
            page.update()
            asyncio.run(show_auto_closing_dialog(page, canceled_dialog, 1.0))

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Setup Already Exists"),
            content=ft.Text("A previous setup already exists.\nDo you want to reset it?"),
            actions=[
                ft.TextButton("Cancel", on_click=reset_canceled),
                ft.TextButton("Reset", on_click=reset_confirmed)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialog)
        page.update()
        return

    perform_encryption(page, uri)


def perform_encryption(page: ft.Page, uri: str):
    ensure_directories()
    key = generate_key()
    encrypt_uri(key, uri)

    dialog = default_alert_dialog(
        title=ft.Text("Setup Complete"),
        content=ft.Text("MongoDB credentials have been encrypted and saved successfully."),
        actions=[ft.TextButton("Close", on_click=lambda e: page.window.close())],
        page=page
    )
    page.open(dialog)
    page.update()


"""
Run setup.py to test the only the setup.
Use the following command to run:
py -m chaewon_login.setup
"""

def main(page: ft.Page):
    global error_label

    page.controls.clear()
    apply_setup_page_config(page)

    label = default_text(TextType.TITLE, "MongoDB URI Setup")
    sublabel = default_text(TextType.SUBTITLE, "Enter your MongoDB URI:")

    entry = uri_input_field

    error_label = default_text(TextType.ERROR, "")
    error_label.visible = False  # Initially hidden

    save_btn = default_action_button(
        text="Save & Encrypt",
        on_click=lambda e: handle_setup(page, entry),
    )
    cancel_btn = preset_button(
        DefaultButton.CANCEL,
        on_click=lambda e: page.window.close()
    )
    button_row = default_row([
        save_btn,
        cancel_btn
    ])

    content = default_container([
        label,
        ft.Divider(),
        sublabel,
        entry,
        error_label,
        button_row
    ])
    page.add(content)

if __name__ == "__main__":
    ft.app(target=main)
