import flet as ft
import tkinter as tk

from chaewon_login.ui.components.text import default_input_field, DefaultInputFieldType


def default_column(controls: ft.Control | list[ft.Control] | None = None) -> ft.Column:
    normalized = (
        [controls] if isinstance(controls, ft.Control)
        else controls if isinstance(controls, list)
        else []
    )
    return ft.Column(
        controls=normalized,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

def default_container(content: ft.Control | list[ft.Control] | None = None) -> ft.Container:
    if isinstance(content, list):
        content = default_column(controls=content)
    elif content is None:
        content = ft.Container()  # placeholder to avoid None content error

    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        padding=40,
        expand=True
    )
    
def default_row(controls: ft.Control | list[ft.Control] | None = None) -> ft.Row:
    if controls is None:
        controls = []
    elif not isinstance(controls, list):
        controls = [controls]

    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )


### MOVE TO A SEPARATE SCRIPT WHEN POSSIBLE
def div(
    color: ft.ColorValue = ft.Colors.ON_PRIMARY,
    thickness: ft.OptionalNumber = None
) -> ft.Divider:
    return ft.Divider(
        color=color,
        thickness=thickness
    )


"""
Run containers.py to test how the containers look alongside other UI components.
If in VSCode, run module test with:
py -m chaewon_login.ui.components.containers
"""

def test(page: ft.Page):
    page.title = "Test GUI"
    page.theme_mode = ft.ThemeMode.DARK
    
    test_username_input = default_input_field(DefaultInputFieldType.USERNAME)
    test_password_input = default_input_field(DefaultInputFieldType.PASSWORD)
    
    test_controls = [
        test_username_input,
        test_password_input
    ]
    
    test_column = default_column(controls=test_controls)
    test_container = default_container(content=test_column)
    
    page.add(test_container)
    
if __name__ == "__main__":
    ft.app(target=test)