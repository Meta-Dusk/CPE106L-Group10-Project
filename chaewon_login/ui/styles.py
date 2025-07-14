import flet as ft

DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_INPUT_FIELD_WIDTH = 300

default_text_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=15,
    weight=ft.FontWeight.NORMAL
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
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

def test():
    pass
    
if __name__ == "__main__":
    test()