import flet as ft


DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_INPUT_FIELD_WIDTH = 300

default_text_style = ft.TextStyle(
    size=15,
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.PRIMARY,
    font_family="Roboto"
)

default_title_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=25,
    weight=ft.FontWeight.BOLD
)

default_subtitle_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=18,
    weight=ft.FontWeight.NORMAL
)

def apply_default_page_config(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        font_family="Roboto",
    )
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

default_action_button_style = ft.ButtonStyle(
    overlay_color={"hovered": ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)},
    shape=ft.RoundedRectangleBorder(radius=12),
    elevation={"pressed": 1, "default": 3}
)