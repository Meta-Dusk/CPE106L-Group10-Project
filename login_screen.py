import flet as ft

# Dummy credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

def main(page: ft.Page):
    page.title = "Chaewon's Meet and Greet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Feedback Text
    message = ft.Text(value="", color=ft.Colors.RED)

    # Input fields
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300
    )

    # Login button handler
    def login_click(e):
        if username.value == VALID_USERNAME and password.value == VALID_PASSWORD:
            message.value = "Login successful!"
            message.color = ft.Colors.GREEN
        else:
            message.value = "Invalid username or password."
            message.color = ft.Colors.RED
        page.update()

    # Main content column
    login_form = ft.Column(
        [
            ft.Text(
                "Chaewon demands your login credentials.",
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            username,
            password,
            ft.ElevatedButton(text="Login", on_click=login_click),
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    # Make page fill and center
    page.add(
        ft.Container(
            content=login_form,
            alignment=ft.alignment.center,
            expand=True,  # allows it to resize with the window
        )
    )

# Run the app
ft.app(target=main)
