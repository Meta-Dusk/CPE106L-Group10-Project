import flet as ft
import threading
import asyncio

from app.auth.hashing import hash_password, verify_password
from app.assets.images import set_logo
from app.db.db_manager import init_database, get_current_mode, toggle_db, find_user, insert_user, DBMode
from app.ui.components.containers import default_column, default_container, div, spaced_buttons
from app.ui.components.dialogs import default_notif_dialog
from app.ui.components.text import default_text, DefaultTextStyle, default_input_field, DefaultInputFieldType
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.screens.loading_screen import show_loading_screen
from app.ui.animations import container_setup
from app.ui.styles import apply_default_page_config
from app.ui.screens.shared_ui import theme_toggle_button, mod_toggle_theme
from app.utils import enable_control_after_delay
from app.routing.route_data import PageRoute


def main_login_ui(page: ft.Page):
    # == Login Page setup ==
    page.controls.clear()
    apply_default_page_config(page)
    
    # == UI Components
    text_login = "Already have an account? Login"
    text_register = "Don't have an account? Register"
    current_mode = get_current_mode().value
    text_switch_to_sqlite = f"Switch to SQLite? (Using: {current_mode})"
    text_switch_to_mongo = f"Switch to MongoDB? (Using: {current_mode})"

    login_message = default_text(DefaultTextStyle.TITLE, "Please enter your login credentials.")
    message = ft.Text(value="", color=ft.Colors.ERROR)
    username_input = default_input_field(DefaultInputFieldType.USERNAME)
    password_input = default_input_field(DefaultInputFieldType.PASSWORD)
    confirm_password_input = default_input_field(DefaultInputFieldType.PASSWORD)
    confirm_password_input.label = "Confirm Password"
    confirm_password_input.visible = False
    
    # == Login Setup ==
    is_login = "is_login"
    mode = {is_login: True}

    def clear_errors():
        username_input.error_text = ""
        password_input.error_text = ""
        confirm_password_input.error_text = ""
        message.value = ""

    def set_error(text_field: ft.TextField, text: str):
        text_field.error_text = text

    def show_message(text: str, error: bool = False):
        message.value = text
        if error:
            message.color = ft.Colors.ERROR
        else:
            message.color = ft.Colors.TERTIARY
    
    def switch_mode(e):
        mode[is_login] = not mode[is_login]
        toggle_button.text = text_register if mode[is_login] else text_login
        confirm_password_input.visible = not mode[is_login]
        clear_errors()
        update_button()
        page.update()

    async def login_or_register(e):
        clear_errors()
        
        username = username_input.value.strip()
        password = password_input.value.strip()
        confirm = confirm_password_input.value.strip() if not mode[is_login] else None
        
        # Validate fields
        if not username:
            set_error(username_input, "Username cannot be empty.")
        if not password:
            set_error(password_input, "Password cannot be empty.")
        if not username or not password:
            show_message("Please fill in all fields.", error=True)
            page.update()
            return
        
        if mode[is_login]:  # Login mode
            user = find_user(username)
            if user and verify_password(password, user["password"]):
                show_message(f"Welcome, {username}! (Logged in with {current_mode}.)")
                page.session.set("user_authenticated", True)
                page.session.set("user_id", username)
                page.update()
                await asyncio.sleep(0.5) # Wait for half a second
                page.go(PageRoute.DASHBOARD.value)
            else:
                set_error(username_input, "Username mismatch.")
                set_error(password_input, "Password mismatch.")
                show_message("Invalid username or password.", error=True)
        else:               # Registration mode
            if password != confirm:
                set_error(password_input, "Make sure you typed this correctly.")
                set_error(confirm_password_input, "Mismatched passwords.")
                show_message("Passwords do not match!", error=True)
            elif find_user(username):
                set_error(username_input, "Username already taken.")
                show_message("Username already exists!", error=True)
            else:
                hashed = hash_password(password)
                insert_user(username, hashed)
                switch_mode(None)
                show_message(f"Registration successful! (Registered in {current_mode}.)")
        
        page.update()

    def update_button():
        if mode[is_login]:
            updated_btn = preset_button(DefaultButton.LOGIN, on_click=action_button.on_click)
        else:
            updated_btn = preset_button(DefaultButton.REGISTER, on_click=action_button.on_click)
        
        action_button.text = updated_btn.text
        action_button.icon = updated_btn.icon
        action_button.style = updated_btn.style
        
        action_button.update()

    def reset(e):
        page.controls.clear()
        main_login_ui(page)
        page.update()

    def handle_db_toggle(e):
        show_loading_screen(page, f"Switching to {toggle_db().value}...")

        def toggle_and_notify():
            conn = init_database()

            if conn is None:
                dialog_content_text = "Failed to switch databases. Please try again."
                dialog_title_text = "Error"
                toggle_db()
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

            dialog_content = default_text(DefaultTextStyle.SUBTITLE, dialog_content_text)
            dialog_title = default_text(DefaultTextStyle.TITLE, dialog_title_text)

            dialog = default_notif_dialog(
                title=dialog_title,
                content=dialog_content,
                on_dismiss=reset
            )

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
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[action_button, control_buttons],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
    
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    
    # == Buttons ==
    db_toggle_button = ft.TextButton(
        icon=ft.Icons.CODE_SHARP,
        icon_color=ft.Colors.PRIMARY,
        text=text_switch_to_sqlite if current_mode == DBMode.MONGO.value else text_switch_to_mongo,
        tooltip="Switch between available databases",
        on_click=handle_db_toggle,
        disabled=True
    )
    toggle_button = ft.TextButton(text=text_register, on_click=switch_mode)
    action_button = preset_button(DefaultButton.LOGIN, on_click=login_or_register)
    control_buttons = [theme_toggle, db_toggle_button]
    
    # exit_btn = preset_button(DefaultButton.EXIT, lambda _: page.window.close())
    exit_btn = ft.TextButton("Exit", on_click=lambda _: page.window.close())
    
    top_row = spaced_buttons([exit_btn], control_buttons)
    
    # == Page Form ==
    form = default_column([
        top_row,
        toggleable_logo,
        div(),
        login_message,
        username_input,
        password_input,
        confirm_password_input,
        action_button,
        toggle_button,
        message
    ])

    page.add(default_container(form))
    
    async def delayed_enable_button():
        await enable_control_after_delay(db_toggle_button, 1)
    
    # Limit user from spamming the switch database button
    page.run_task(delayed_enable_button)