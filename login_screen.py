import flet as ft
from pymongo import MongoClient
import bcrypt
import time

MONGODB_CONNECTION_STRING = "localhost:27017" # Adjust if hosted remotely
collection = None

ENCODING_FORMAT = "utf-8"

# Chaewon images
image_sources = {
    "chaewon_stare" : "https://image.koreaboo.com/2025/04/Header-Image-2025-04-08T171312.835.jpg",
    "chaewon_side" : "https://koreajoongangdaily.joins.com/data/photo/2022/04/07/3e7dd04f-cadc-4336-9577-95a96e153801.jpg",
    "chaewon_sad" : "https://i.pinimg.com/736x/33/63/84/336384d11ac51be54c6b6b64cb93ff7e.jpg"
}

text_label_size = 25
input_field_width = 300

default_image = ft.Image(
    src=image_sources["chaewon_stare"],
    width=150,
    height=150,
    border_radius=75,
    fit=ft.ImageFit.COVER,
    gapless_playback=True,
)

def connect_to_mongo():
    try:
        client = MongoClient(
            f"mongodb://{MONGODB_CONNECTION_STRING}/",
            serverSelectionTimeoutMS=2000
        )
        client.admin.command("ping")  # Check if the server is reachable
        db = client["ProjectATS"]
        return db["accounts"]
    except Exception as e:
        print("MongoDB connection failed:", e)
        return None

def check_mongo_connection(page):
    global collection
    collection = connect_to_mongo()
    
    image_sad_chaewon = default_image
    image_sad_chaewon.src = image_sources["chaewon_sad"]
    
    warning_message = ft.Text("Failed to connect to MongoDB.", color=ft.Colors.RED, size=text_label_size)
    warning_subtitle = ft.Text(f"Please ensure the MongoDB server is running on {MONGODB_CONNECTION_STRING}.")
    
    def retry_connection(e):
        page.controls.clear()
        page.update()
        if not check_mongo_connection(page):
            return
        main_login_ui(page)  # continue to full UI if retry succeeds
    
    retry_button = ft.ElevatedButton(text="Retry Connection", on_click=retry_connection)
    
    if collection is None:
        form = ft.Column(
            [
                image_sad_chaewon,
                warning_message,
                warning_subtitle,
                retry_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
        
        page.add(
            ft.Container(
                content=form,
                alignment=ft.alignment.center,
                expand=True,
                # bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED),
            )
        )
        
        return False
    return True

def main_login_ui(page):
    text_login = "Already have an account? Login"
    text_register = "Don't have an account? Register"
    
    # UI components
    login_message = ft.Text(
        "Chaewon demands your login credentials.",
        size=text_label_size,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    message = ft.Text(value="", color=ft.Colors.RED)
    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=input_field_width
    )
    confirm_password_input = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=input_field_width,
        visible=False
    )
    
    current_image = default_image
    current_image.src = image_sources["chaewon_stare"]
    
    # Animated container with fade + scale + rotation
    toggleable_chaewon = ft.Container(
        content=current_image,
        animate_opacity=300,
        animate_scale=500,
        animate_rotation=500,
        scale=0.8,       # initial zoom (smaller)
        opacity=1.0,     # start visible
        rotate=0.0,      # no spin initially
        alignment=ft.alignment.center,
    )
    
    def chaewon_toggle(e=None):
        # Step 1: Fade out and shrink slightly
        toggleable_chaewon.opacity = 0.0
        toggleable_chaewon.scale = 0.7
        page.update()
        time.sleep(0.2)

        # Step 2: Swap the image
        if current_image.src == image_sources["chaewon_stare"]:
            current_image.src = image_sources["chaewon_side"]
        else:
            current_image.src = image_sources["chaewon_stare"]

        toggleable_chaewon.content = current_image
        page.update()

        # Step 3: Dramatic entrance – scale up, rotate, fade in
        toggleable_chaewon.opacity = 1.0
        toggleable_chaewon.scale = 1.2
        toggleable_chaewon.rotate = 0.15
        page.update()
        time.sleep(0.3)

        # Step 4: Return to normal size/rotation
        toggleable_chaewon.scale = 1.0
        toggleable_chaewon.rotate = 0.0
        page.update()
    
    # Toggle between light and dark modes
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.Icons.LIGHT_MODE
            chaewon_toggle(e)
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.Icons.DARK_MODE
            chaewon_toggle(e)
        page.update()

    # Toggle between login and register mode
    mode = {"is_login": True}
    toggle_button = ft.TextButton(text=text_register)

    def switch_mode(e):
        mode["is_login"] = not mode["is_login"]
        if mode["is_login"]:
            toggle_button.text = text_register
            confirm_password_input.visible = False
        else:
            toggle_button.text = text_login
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
                    password.encode(ENCODING_FORMAT), bcrypt.gensalt()).decode(ENCODING_FORMAT)
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
        icon=ft.Icons.LIGHT_MODE,
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

# Hash password for storing
def hash_password(password):
    return bcrypt.hashpw(password.encode(ENCODING_FORMAT), bcrypt.gensalt()).decode(ENCODING_FORMAT)

# Check hashed password
def verify_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode(ENCODING_FORMAT)  # only encode if it's a string
    return bcrypt.checkpw(password.encode(ENCODING_FORMAT), hashed)

# Main Flet App
def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    # page.window_width = 400
    # page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    if not check_mongo_connection(page):
        return # Stop app setup if MongoDB is unreachable

    main_login_ui(page)

# Run app
ft.app(target=main)