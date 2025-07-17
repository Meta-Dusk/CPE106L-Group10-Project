import time
import flet as ft
import threading

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
from chaewon_login.ui.components.containers import default_column, default_container
from chaewon_login.ui.components.dialogs import default_notif_dialog
from chaewon_login.ui.components.text import (
    default_text,
    TextType,
    default_input_field,
    InputFieldType
)
from chaewon_login.ui.route_data import PageRoute
from chaewon_login.ui.loading_screen import show_loading_screen

def main_login_ui(page: ft.Page):
    page.controls.clear()
    page.scroll = ft.ScrollMode.AUTO
    text_login = "Already have an account? Login"
    text_register = "Don't have an account? Register"
    current_mode = get_current_mode().value
    text_switch_to_sqlite = f"Switch to SQLite (Currently {current_mode})"
    text_switch_to_mongo = f"Switch to MongoDB (Currently {current_mode})"

    login_message = default_text(TextType.TITLE, "Chaewon demands your login credentials.")
    login_message.color = ft.Colors.PRIMARY
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
        opacity=1.0,
        rotate=0.0,
        alignment=ft.alignment.center,
    )

    def chaewon_toggle(e=None):
        chaewon_stare = ImageData.CHAEWON_STARE.value
        chaewon_side = ImageData.CHAEWON_SIDE.value
        toggleable_chaewon.opacity = 0.0
        toggleable_chaewon.scale = 0.8
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
                page.session.set("user_authenticated", True)
                page.session.set("user_id", username)
                page.go(PageRoute.DASHBOARD.value)
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
        # Show the loading screen right away
        show_loading_screen(page, f"Switching to {toggle_db().value}...")

        def toggle_and_notify():
            # Attempt to initialize database
            conn = init_database()

            # Determine result message
            if conn is None:
                dialog_content_text = "Failed to switch databases. Please try again."
                dialog_title_text = "Error"
                toggle_db()  # Revert back
                init_database()
            else:
                current_mode = get_current_mode()
                if current_mode == DBMode.SQLITE:
                    dialog_content_text = f"You are now using {current_mode.value}."
                    dialog_title_text = "Database Switched"
                    db_toggle_button.text = text_switch_to_mongo
                else:
                    dialog_content_text = f"You are now using {current_mode.value}."
                    dialog_title_text = "Database Switched"
                    db_toggle_button.text = text_switch_to_sqlite

            # Build dialog content
            dialog_content = default_text(TextType.SUBTITLE, dialog_content_text)
            dialog_title = default_text(TextType.TITLE, dialog_title_text)

            dialog = default_notif_dialog(
                title=dialog_title,
                content=dialog_content,
                on_dismiss=reset
            )

            # Return to main thread to update UI
            page.controls.clear()
            page.add(default_container(form))
            page.open(dialog)
            page.update()
            
            # Auto-close after n amount of seconds
            def auto_close():
                page.close(dialog)
                page.update()

            threading.Timer(1.0, auto_close).start()

        # Run DB switching logic in a background thread
        threading.Thread(target=toggle_and_notify).start()


    db_toggle_button = ft.TextButton(
        icon=ft.Icons.CODE_SHARP,
        text=text_switch_to_sqlite if current_mode == DBMode.MONGO.value else text_switch_to_mongo,
        tooltip="Switch between available databases",
        on_click=handle_db_toggle
    )

    form = default_column(controls=
        [
            ft.Row([theme_toggle, db_toggle_button], alignment=ft.MainAxisAlignment.END),
            toggleable_chaewon,
            login_message,
            ft.Divider(color=ft.Colors.ON_PRIMARY),
            username_input,
            password_input,
            confirm_password_input,
            action_button,
            toggle_button,
            message,
        ]
    )

    page.add(default_container(form))
