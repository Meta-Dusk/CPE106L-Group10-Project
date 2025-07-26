import flet as ft
import shutil
import asyncio
import subprocess

from cryptography.fernet import Fernet
from app.config import Config
from app.assets.audio_manager import audio, setup_audio, SFX
from app.setup_env import setup_env
from app.ui.styles import apply_setup_page_config
from app.ui.components.containers import default_container, default_row, default_column, div
from app.ui.components.text import default_text, DefaultTextStyle, default_input_field, DefaultInputFieldType
from app.ui.components.buttons import default_action_button, preset_button, DefaultButton
from app.ui.components.dialogs import default_alert_dialog, show_auto_closing_dialog
from pymongo.uri_parser import parse_uri
from pymongo import MongoClient


def validate_mongo_uri(uri: str) -> bool:
    try:
        parse_uri(uri)  # Validate format
        # Optionally test connection
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.server_info()
        return True
    except Exception as e:
        print(f"[MongoDB Error] {e}")
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


def handle_setup(
    page: ft.Page, entry: ft.TextField, input_mode: dict,
    username_input=None, password_input=None, host_input=None
):
    if input_mode["login"]:
        # Build URI from parts
        username = username_input.value.strip()
        password = password_input.value.strip()
        host = host_input.value.strip()

        if not all([username, password, host]):
            for f in [username_input, password_input, host_input]:
                if not f.value.strip():
                    f.error_text = "This field is required."
            audio.play_sfx(SFX.ERROR)
            page.update()
            return
        audio.play_sfx(SFX.REWARD)
        uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
    else:
        audio.play_sfx(SFX.ERROR)
        uri = entry.value.strip()
        if not uri:
            entry.error_text = "MongoDB URI cannot be empty."
            page.update()
            return

    # URI validation
    if not validate_mongo_uri(uri):
        (entry if not input_mode["login"] else host_input).error_text = "Invalid MongoDB URI format."
        page.update()
        return

    setup_env()

    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        def reset_confirmed(e):
            page.close(dialog)
            error_check = delete_directories()
            if error_check is not True:
                entry.error_text = error_check
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
        actions=[ft.TextButton("Close", on_click=lambda e: run_launcher(page))],
        page=page
    )
    page.open(dialog)
    page.update()
    
def run_launcher(page: ft.Page):
    audio.play_sfx(SFX.CLICK)
    audio.stop_bgm()
    page.window.close()
    subprocess.run(["py", "-m", "launch"], check=True)


"""
Run setup.py to test only the setup.
Use the following command to run:
py -m app.setup
"""

def main(page: ft.Page):
    setup_audio()
    audio.on_ready(lambda: audio.play_random_bgm())
    page.controls.clear()
    apply_setup_page_config(page)
    
    def switch_mode():
        input_mode["login"] = not input_mode["login"]
        inputs_column.controls.clear()

        if input_mode["login"]:
            sublabel.value = "Enter your MongoDB Credentials:"
            inputs_column.controls.extend([username_input, password_input, host_input])
        else:
            sublabel.value = "Enter your MongoDB URI:"
            inputs_column.controls.append(entry)
        
        entry.error_text = ""
        apply_setup_page_config(page, alt=input_mode["login"])
        page.update()

    
    input_mode = {"login": False}
    
    username_input = default_input_field(DefaultInputFieldType.USERNAME)
    password_input = default_input_field(DefaultInputFieldType.PASSWORD)
    host_input = default_input_field(DefaultInputFieldType.HOST)

    label = default_text(DefaultTextStyle.TITLE, "MongoDB URI Setup")
    sublabel = default_text(DefaultTextStyle.SUBTITLE, "Enter your MongoDB URI:")

    entry = default_input_field(DefaultInputFieldType.URI)
    
    inputs_column = default_column([entry])

    save_btn = default_action_button(
        text="Save & Encrypt",
        on_click=lambda e: handle_setup(
            page,
            entry,
            input_mode,
            username_input,
            password_input,
            host_input
        )
    )
    cancel_btn = preset_button(
        DefaultButton.CANCEL,
        on_click=lambda e: run_launcher(page)
    )
    switch_btn = default_action_button(
        text="Switch Mode",
        icon=ft.Icons.DATASET,
        tooltip="Switch input modes",
        on_click=lambda e: switch_mode()
    )
    button_row = default_row([
        save_btn,
        switch_btn,
        cancel_btn
    ])

    content = default_container([
        label,
        div(),
        sublabel,
        inputs_column,
        button_row
    ])
    page.add(content)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="app/assets")
