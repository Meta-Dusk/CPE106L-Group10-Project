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
from app.ui.components.dialogs import default_alert_dialog, show_auto_closing_dialog, default_notif_dialog
from pymongo.uri_parser import parse_uri
from pymongo import MongoClient


LOGIN = "login"


def validate_mongo_uri(uri: str) -> bool:
    try:
        parse_uri(uri)  # Validate format
        # Optionally test connection
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.server_info()
        return True
    except Exception as e:
        error = f"[MongoDB Error] {e}"
        print(error)
        return error

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
    page: ft.Page, entry: ft.TextField, input_mode: dict[str, bool],
    username_input=ft.TextField, password_input=ft.TextField, host_input=ft.TextField
):
    if input_mode[LOGIN]:
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
        uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority&appName=TestCluster"
    else:
        audio.play_sfx(SFX.ERROR)
        uri = entry.value.strip()
        if not uri:
            entry.error_text = "MongoDB URI cannot be empty."
            page.update()
            return

    # URI validation
    check_validation = validate_mongo_uri(uri)
    if check_validation is not True:
        if not input_mode[LOGIN]:
            entry.error_text = "Invalid MongoDB URI format."
        else:
            for input in [username_input, password_input, host_input]:
                input.error_text = "Something went wrong."
        audio.play_sfx(SFX.ERROR)
        error_dialog = default_notif_dialog(
            title="Setup Error",
            content=default_text(DefaultTextStyle.ERROR, text=f"{check_validation}")
        )
        page.open(error_dialog)
        page.update()
        return

    setup_env()

    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        entry.error_text = ""
        def reset_confirmed(e):
            page.close(dialog)
            error_check = delete_directories()
            if error_check is not True:
                entry.error_text = "Something went wrong."
                notif_dialog = default_notif_dialog(
                    title="File Error",
                    content=default_text(DefaultTextStyle.ERROR, text=f"{error_check}")
                )
                page.open(notif_dialog)
            else:
                perform_encryption(page, uri)
            page.update()

        def reset_canceled(e):
            page.close(dialog)
            audio.play_sfx(SFX.NOTIF)
            canceled_dialog = default_notif_dialog(
                title="Setup Canceled",
                content=default_text(DefaultTextStyle.SUBTITLE, "Setup canceled. No changes were made.")
            )
            asyncio.run(show_auto_closing_dialog(page, canceled_dialog, 1.0))

        dialog = default_alert_dialog(
            title="Setup Already Exists",
            content=default_text(DefaultTextStyle.SUBTITLE, "Do you want to reset previous setup?"),
            actions=[
                default_action_button(text="Cancel", on_click=reset_canceled, auto_focus=True),
                default_action_button(text="Reset", on_click=reset_confirmed)
            ],
            page=page
        )
        audio.play_sfx(SFX.ALERT)
        page.open(dialog)
        page.update()
        return

    perform_encryption(page, uri)


def perform_encryption(page: ft.Page, uri: str):
    ensure_directories()
    key = generate_key()
    encrypt_uri(key, uri)

    close_btn = default_action_button(
        text="Close",
        on_click=lambda e: run_launcher(page),
        auto_focus=True
    )
    dialog = default_alert_dialog(
        title=ft.Text("Setup Complete"),
        content=ft.Text("MongoDB credentials have been encrypted and saved successfully."),
        actions=[close_btn],
        page=page
    )
    audio.play_sfx(SFX.REWARD)
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
        input_mode[LOGIN] = not input_mode[LOGIN]
        inputs_column.controls.clear()

        if input_mode[LOGIN]:
            sublabel.value = "Enter your MongoDB Credentials:"
            inputs_column.controls.extend([username_input, password_input, host_input])
        else:
            sublabel.value = "Enter your MongoDB URI:"
            inputs_column.controls.append(entry)
        
        entry.error_text = ""
        apply_setup_page_config(page, alt=input_mode[LOGIN])
        page.update()

    
    input_mode = {LOGIN: False}
    
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
    button_row = default_row([save_btn, switch_btn, cancel_btn])

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
