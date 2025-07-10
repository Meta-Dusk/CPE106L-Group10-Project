import time
import flet as ft

from auth.encryption import hash_password, verify_password
from assets.images import image_sources, default_image
from constants import DBMode, text_label_size, text_subtitle_size, input_field_width
from db.db_manager import init_database, get_current_mode, toggle_db, find_user, insert_user

def main_login_ui(page: ft.Page):
    text_login = "Already have an account? Login"
    text_register = "Don't have an account? Register"

    login_message = ft.Text(
        "Chaewon demands your login credentials.",
        size=text_label_size,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    message = ft.Text(value="", color=ft.Colors.RED)
    username_input = ft.TextField(label="Username", width=input_field_width)
    password_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=input_field_width)
    confirm_password_input = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=input_field_width, visible=False)

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
        toggleable_chaewon.opacity = 0.0
        toggleable_chaewon.scale = 0.7
        page.update()
        time.sleep(0.2)

        current_image.src = image_sources["chaewon_side"] if current_image.src == image_sources["chaewon_stare"] else image_sources["chaewon_stare"]
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

    mode = {"is_login": True}
    toggle_button = ft.TextButton(text=text_register)

    def switch_mode(e):
        mode["is_login"] = not mode["is_login"]
        toggle_button.text = text_register if mode["is_login"] else text_login
        confirm_password_input.visible = not mode["is_login"]
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
        elif mode["is_login"]:
            user = find_user(username)
            if user and verify_password(password, user["password"]):
                message.value = f"Welcome, {username}! Using {get_current_mode().value}"
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
                message.value = f"Registration successful! Now using {get_current_mode().value}"
                message.color = ft.Colors.GREEN
                switch_mode(None)

        page.update()

    action_button = ft.ElevatedButton(text="Login", on_click=login_or_register)

    def update_button_text():
        action_button.text = "Login" if mode["is_login"] else "Register"
        page.update()

    theme_toggle = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Toggle Theme",
        on_click=toggle_theme
    )
    
    def handle_db_toggle(e):
        toggle_db()
        init_database()
        
        dialog_content_text = "You are now using " + get_current_mode().value + "."
        dialog_content = ft.Text(dialog_content_text, text_align=ft.TextAlign.CENTER, size=text_subtitle_size)
        
        if get_current_mode() == DBMode.SQLITE:
            dialog_content.color = ft.Colors.BLUE
        else:
            dialog_content.color = ft.Colors.PINK
        
        dialog = ft.AlertDialog(
            title=ft.Text("Database Switched", text_align=ft.TextAlign.CENTER, size=text_label_size, weight=ft.FontWeight.BOLD),
            content=dialog_content,
            alignment=ft.alignment.center,
            on_dismiss=lambda e: page.update(),
            title_padding=ft.padding.all(25),
            adaptive=True,
            icon=ft.Icon(name=ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE),
            # icon_padding=ft.padding.all(10),
        )
        page.open(dialog)
        page.update()

    db_toggle_button = ft.TextButton(text="Switch DB", on_click=handle_db_toggle)


    form = ft.Column(
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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    page.add(ft.Container(content=form, alignment=ft.alignment.center, expand=True))
