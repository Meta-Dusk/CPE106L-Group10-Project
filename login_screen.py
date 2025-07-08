import flet as ft
from pymongo import MongoClient
import bcrypt
import time

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Adjust if hosted remotely
db = client["ProjectATS"]
collection = db["accounts"]

# Hash password for storing
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Check hashed password
def verify_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")  # only encode if it's a string
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

# Main Flet App
def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"

    # UI components
    login_message = ft.Text(
        "Chaewon demands your login credentials.",
        size=20,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    message = ft.Text(value="", color=ft.Colors.RED)
    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300
    )
    confirm_password_input = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=300,
        visible=False
    )
    
    # Chaewon toggle
    image_sources = {
        "chaewon_stare" : "https://image.koreaboo.com/2025/04/Header-Image-2025-04-08T171312.835.jpg",
        "chaewon_side" : "https://koreajoongangdaily.joins.com/data/photo/2022/04/07/3e7dd04f-cadc-4336-9577-95a96e153801.jpg"
    }
    current_image = {"src": image_sources["chaewon_stare"]}
    
    # AnimatedSwitcher wrapper
    toggleable_chaewon = ft.AnimatedSwitcher(
        duration=500,
        transition=ft.AnimatedSwitcherTransition.FADE,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        content=ft.Image(
            src=current_image["src"],
            width=150,
            height=150,
            border_radius=75,
            fit=ft.ImageFit.COVER,
            key=current_image["src"]  # must use key for animation to trigger
        ),
    )
    
    def chaewon_toggle(e=None):
    # Swap the image source
        if current_image["src"] == image_sources["chaewon_stare"]:
            current_image["src"] = image_sources["chaewon_side"]
        else:
            current_image["src"] = image_sources["chaewon_stare"]

        # Animate by replacing the content of AnimatedSwitcher
        toggleable_chaewon.content = ft.Image(
            src=current_image["src"],
            width=150,
            height=150,
            border_radius=75,
            fit=ft.ImageFit.COVER,
            key=current_image["src"]
        )
        page.update()

    
    # Toggle between light and dark modes
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.Icons.DARK_MODE
            chaewon_toggle(e)
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.Icons.LIGHT_MODE
            chaewon_toggle(e)
        page.update()

    # Toggle between login and register mode
    mode = {"is_login": True}
    toggle_button = ft.TextButton(text="Don't have an account? Register")

    def switch_mode(e):
        mode["is_login"] = not mode["is_login"]
        if mode["is_login"]:
            toggle_button.text = "Don't have an account? Register"
            confirm_password_input.visible = False
        else:
            toggle_button.text = "Already have an account? Login"
            confirm_password_input.visible = True
        message.value = ""
        page.update()

    toggle_button.on_click = switch_mode

    def login_or_register(e):
        username = username_input.value.strip()
        password = password_input.value.strip()

        if not username or not password:
            message.value = "Please fill in all fields."
            message.color = ft.Colors.RED
            page.update()
            return

        if mode["is_login"]:
            user = collection.find_one({"username": username})
            if user and verify_password(password, user["password"]):
                message.value = f"Welcome, {username}!"
                message.color = ft.Colors.GREEN
            else:
                message.value = "Invalid username or password."
                message.color = ft.Colors.RED
        else:
            confirm = confirm_password_input.value.strip()
            if password != confirm:
                message.value = "Passwords do not match!"
                message.color = ft.Colors.RED
            elif collection.find_one({"username": username}):
                message.value = "Username already exists!"
                message.color = ft.Colors.RED
            else:
                hashed = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                collection.insert_one({"username": username, "password": hashed})
                message.value = "Registration successful! Please log in."
                message.color = ft.Colors.GREEN
                switch_mode(None)
                update_button_text()

        page.update()

    action_button = ft.ElevatedButton(text="Login", on_click=login_or_register)

    # Update action button text based on mode
    def update_button_text():
        action_button.text = "Login" if mode["is_login"] else "Register"
        page.update()

    toggle_button.on_click = lambda e: (switch_mode(e), update_button_text())

    theme_toggle = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Toggle Theme",
        on_click=toggle_theme
    )

    form = ft.Column(
        [
            theme_toggle,
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

# Run app
ft.app(target=main)