import flet as ft

from typing import Optional


def default_column(
    controls: Optional[ft.Control | list[ft.Control]] = None,
    expand: bool = True
) -> ft.Column:
    normalized = (
        [controls] if isinstance(controls, ft.Control)
        else controls if isinstance(controls, list)
        else []
    )
    return ft.Column(
        controls=normalized,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=expand
    )

def default_container(
    content: Optional[ft.Control | list[ft.Control]] = None,
    expand: bool = True,
    padding: Optional[ft.PaddingValue] = 40,
    width: Optional[ft.OptionalNumber] = None,
    height: Optional[ft.OptionalNumber] = None
) -> ft.Container:
    if isinstance(content, list):
        content = default_column(controls=content)
    elif content is None:
        content = ft.Container()  # placeholder to avoid None content error

    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        padding=padding,
        expand=expand,
        width=width,
        height=height
    )
    
def default_row(
    controls: Optional[ft.Control | list[ft.Control]] = None,
    spacing: ft.OptionalNumber = 20
) -> ft.Row:
    if controls is None:
        controls = []
    elif not isinstance(controls, list):
        controls = [controls]

    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=spacing
    )
    
def spaced_buttons(
    left_controls: Optional[list[ft.Control]] = None,
    right_controls: Optional[list[ft.Control]] = None,
    spacing: ft.OptionalNumber = 10
) -> ft.Row:
    """
    Provides spacing for two sets of buttons; separated into left only and right only buttons.
    
    Args:
        left_controls (list[`ft.Control`]): Can be `None`, or have any controls, such as buttons (Like the `exit_btn`). Must be a list of controls.
        left_controls (list[`ft.Control`]): Also can be `None`. I usually put buttons such as the theme button here. Must be a list of controls.
        
    Returns:
        `ft.Row`: A row that is spaced evenly. Controls are placed at either left or right side only
    """
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

