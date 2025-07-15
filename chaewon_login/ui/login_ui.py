import time
import flet as ft

from chaewon_login.auth.hashing import hash_password, verify_password
from chaewon_login.assets.images import ImageData, default_image
from chaewon_login.db.db_manager import (
    init_database,
    get_current_mode,
    toggle_db,
    find_user,
    insert_user,
    DBMode
)
from chaewon_login.ui.components import (
    default_input_field,
    InputFieldType,
    default_text,
    TextType,
    default_column,
    default_container,
    default_alert_dialog
)

def main_login_ui(page: ft.Page):
    page.controls.clear()
    text_login = "Already have an account? Login"
    text_register = "Don't have an account? Register"
    current_mode = get_current_mode().value
    text_switch_to_sqlite = f"Switch to SQLite (Currently {current_mode})"
    text_switch_to_mongo = f"Switch to MongoDB (Currently {current_mode})"

    login_message = default_text(TextType.TITLE, "Chaewon demands your login credentials.")
    message = ft.Text(value="", color=ft.Colors.RED)
    username_input = default_input_field(InputFieldType.USERNAME)
    password_input = default_input_field(InputFieldType.PASSWORD)
    confirm_password_input = default_input_field(InputFieldType.PASSWORD)
    confirm_password_input.label = "Confirm Password"
    confirm_password_input.visible = False

    current_image = default_image()

    toggleable_chaewon = ft.Container(
        content=current_image,
        animate_opacity=300,
        animate_scale=500,
        animate_rotation=500,
        scale=0.8,
        opacity=1.0,
        rotate=0.0,
        alignment=ft.alignment.center,
    )

    def chaewon_toggle(e=None):
        chaewon_stare = ImageData.CHAEWON_STARE.value
        chaewon_side = ImageData.CHAEWON_SIDE.value
        toggleable_chaewon.opacity = 0.0
        toggleable_chaewon.scale = 0.7
        page.update()
        time.sleep(0.2)
        
        if current_image.src == chaewon_stare.path:
            current_image.src = chaewon_side.path
            current_image.tooltip = chaewon_side.description
        else:
            current_image.src = chaewon_stare.path
            current_image.tooltip = chaewon_stare.description
        
        toggleable_chaewon.content = current_image
        page.update()

        toggleable_chaewon.opacity = 1.0
        toggleable_chaewon.scale = 1.2
        toggleable_chaewon.rotate = 0.15
        page.update()
        time.sleep(0.3)

        toggleable_chaewon.scale = 1.0
        toggleable_chaewon.rotate = 0.0
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.Icons.DARK_MODE
        chaewon_toggle(e)
        page.update()
        
    is_login = "is_login"
    mode = {is_login: True}
    toggle_button = ft.TextButton(text=text_register)

    def switch_mode(e):
        mode[is_login] = not mode[is_login]
        toggle_button.text = text_register if mode[is_login] else text_login
        confirm_password_input.visible = not mode[is_login]
        message.value = ""
        update_button_text()
        page.update()

    toggle_button.on_click = switch_mode

    def login_or_register(e):
        username = username_input.value.strip()
        password = password_input.value.strip()

        if not username or not password:
            message.value = "Please fill in all fields."
            message.color = ft.Colors.RED
        elif mode[is_login]:
            user = find_user(username)
            if user and verify_password(password, user["password"]):
                message.value = f"Welcome, {username}! (Logged in with {current_mode}.)"
                message.color = ft.Colors.GREEN
            else:
                message.value = "Invalid username or password."
                message.color = ft.Colors.RED
        else:
            confirm = confirm_password_input.value.strip()
            if password != confirm:
                message.value = "Passwords do not match!"
                message.color = ft.Colors.RED
            elif find_user(username):
                message.value = "Username already exists!"
                message.color = ft.Colors.RED
            else:
                hashed = hash_password(password)
                insert_user(username, hashed)
                switch_mode(None)
                message.value = f"Registration successful! (Registered in {current_mode}.)"
                message.color = ft.Colors.GREEN

        page.update()

    action_button = ft.ElevatedButton(text="Login", on_click=login_or_register)

    def update_button_text():
        action_button.text = "Login" if mode[is_login] else "Register"
        page.update()

    theme_toggle = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Toggle Theme",
        on_click=toggle_theme
    )
    
    def reset(e):
        page.controls.clear()
        main_login_ui(page)
        page.update()
    
    def handle_db_toggle(e):
        dialog_content_text = f"You are now using {toggle_db().value}."
        collection = init_database(page)
        dialog_title_text = "Database Switched"
        dialog_content_color = ft.Colors.BLUE
        
        if collection is None:
            dialog_content_color = ft.Colors.RED
            dialog_content_text = "Failed to switch databases. Please try again."
            dialog_title_text = "Error"
            toggle_db()
            collection = init_database()
        elif get_current_mode() == DBMode.SQLITE:
            dialog_content_color = ft.Colors.BLUE
            db_toggle_button.text = text_switch_to_mongo
        else:
            dialog_content_color = ft.Colors.PINK
            db_toggle_button.text = text_switch_to_sqlite
            
        dialog_content = default_text(TextType.TITLE, dialog_content_text)
        dialog_content.color = dialog_content_color
        
        dialog_title = default_text(TextType.TITLE, dialog_title_text)
        dialog = default_alert_dialog(
            title=dialog_title,
            content=dialog_content,
            on_dismiss=reset
        )
        # dialog = ft.AlertDialog(
        #     title=dialog_title,
        #     content=dialog_content,
        #     alignment=ft.alignment.center,
        #     on_dismiss=reset,
        #     title_padding=ft.padding.all(25),
        #     adaptive=True,
        #     icon=ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
        # )
        page.open(dialog)
        page.update()

    db_toggle_button = ft.TextButton(
        icon=ft.Icons.CODE_SHARP,
        text=text_switch_to_sqlite if current_mode == DBMode.MONGO.value else text_switch_to_mongo,
        tooltip="Switch between available databases",
        on_click=handle_db_toggle
    )

    form = default_column(controls=
        [
            theme_toggle,
            db_toggle_button,
            toggleable_chaewon,
            login_message,
            username_input,
            password_input,
            confirm_password_input,
            action_button,
            toggle_button,
            message,
        ]
    )

    page.add(default_container(form))
