import flet as ft
from chaewon_login.assets.images import ICON_PATH


DEFAULT_FONT_FAMILY = "Roboto"
DEFAULT_INPUT_FIELD_WIDTH = 300
APP_NAME = "Chae.App"


# == Text Styles ==
default_text_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=15,
    weight=ft.FontWeight.NORMAL,
    color=ft.Colors.ON_SECONDARY,
)

default_title_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=25,
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.ON_PRIMARY,
)

default_subtitle_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=18,
    weight=ft.FontWeight.NORMAL,
    color=ft.Colors.ON_SECONDARY,
)


# == Page Styles and Configs ==
def apply_default_page_config(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.DEEP_PURPLE,
        font_family=DEFAULT_FONT_FAMILY,
    )
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.center()
    page.window.icon = ICON_PATH.as_posix()

def static_page_config(page: ft.Page):
    apply_default_page_config(page)
    page.window.to_front()
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = False

def default_page_border(page: ft.Page):
    page.decoration = ft.BoxDecoration(
        border=ft.border.all(5, ft.Colors.PRIMARY),
    )

def apply_launcher_page_config(page: ft.Page):
    static_page_config(page)
    default_page_border(page)
    page.title = f"{APP_NAME} | Launcher"
    page.window.width = 320
    page.window.height = 350
    
def apply_setup_page_config(page: ft.Page):
    static_page_config(page)
    default_page_border(page)
    page.title = f"{APP_NAME} | Setup"
    page.window.width = 600
    page.window.height = 350


# == Border Styles
def border_side(
    width: int = 2,
    color: ft.ColorValue = ft.Colors.PRIMARY_CONTAINER
) -> ft.BorderSide:
    return ft.BorderSide(
        width=width,
        color=color,
        stroke_align=ft.BorderSideStrokeAlign.CENTER
    )


# == Button Styles
default_action_button_style = ft.ButtonStyle(
    animation_duration=200,
    icon_color=ft.Colors.ON_SECONDARY,
    icon_size=15,
    bgcolor=ft.Colors.PRIMARY,
    shape={
        ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(ft.border_radius.all(12)),
        ft.ControlState.PRESSED: ft.RoundedRectangleBorder(ft.border_radius.all(8))
    },
    side={
        ft.ControlState.DEFAULT: border_side(color=ft.Colors.PRIMARY),
        ft.ControlState.FOCUSED: border_side(),
    },
    overlay_color={
        ft.ControlState.HOVERED: ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
        ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE),
        ft.ControlState.PRESSED: ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE),
    },
    elevation={
        ft.ControlState.DEFAULT: 1,
        ft.ControlState.DISABLED: 0
    }
)
