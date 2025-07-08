import flet as ft
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Adjust if hosted remotely
db = client["ProjectATS"]
collection = db["accounts"]

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    message = ft.Text(value="", color=ft.Colors.RED)

    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300
    )

    def login_click(e):
        username = username_input.value
        password = password_input.value

        # Check MongoDB for matching credentials
        user = collection.find_one({"username": username, "password": password})
        if user:
            message.value = f"Welcome, {username}!"
            message.color = ft.Colors.GREEN
        else:
            message.value = "Invalid username or password."
            message.color = ft.Colors.RED
        page.update()

    login_form = ft.Column(
        [
            ft.Text(
                "Chaewon demands your login credentials.",
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            username_input,
            password_input,
            ft.ElevatedButton(text="Login", on_click=login_click),
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    page.add(
        ft.Container(
            content=login_form,
            alignment=ft.alignment.center,
            expand=True,
        )
    )

ft.app(target=main)
