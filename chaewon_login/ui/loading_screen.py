import flet as ft
from constants import TEXT_LABEL_SIZE

def show_loading_screen(page: ft.Page, message: str = "Connecting..."):
    loading_text = ft.Text(message, size=TEXT_LABEL_SIZE)
    loading_spinner = ft.ProgressRing()

    loading_ui = ft.Column(
        [loading_spinner, loading_text],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    page.add(ft.Container(content=loading_ui, alignment=ft.alignment.center, expand=True))
    page.update()
