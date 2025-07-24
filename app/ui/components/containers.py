import flet as ft

from typing import Optional


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
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
    
def spaced_buttons(
    left_controls: Optional[list[ft.Control]] = None,
    right_controls: Optional[list[ft.Control]] = None,
    spacing: ft.OptionalNumber = 10
) -> ft.Row:
    left_row = ft.Row(
        controls=left_controls,
        alignment=ft.MainAxisAlignment.START,
        spacing=spacing
    )
    right_row = ft.Row(
        controls=right_controls,
        alignment=ft.MainAxisAlignment.END,
        spacing=spacing
    )
    return ft.Row(
        controls=[left_row, right_row],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )


### MOVE TO A SEPARATE SCRIPT WHEN POSSIBLE
def div(
    color: ft.ColorValue = ft.Colors.PRIMARY,
    thickness: ft.OptionalNumber = None
) -> ft.Divider:
    return ft.Divider(
        color=color,
        thickness=thickness
    )

