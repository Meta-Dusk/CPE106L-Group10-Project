import flet as ft
from chaewon_login.assets.images import ICON_PATH
from chaewon_login.ui.theme_service import load_theme_mode


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
    color=ft.Colors.PRIMARY,
)
default_subtitle_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=18,
    weight=ft.FontWeight.NORMAL,
    color=ft.Colors.ON_PRIMARY_CONTAINER,
)
default_error_text_style = ft.TextStyle(
    font_family=DEFAULT_FONT_FAMILY,
    size=18,
    weight=ft.FontWeight.NORMAL,
    color=ft.Colors.ON_ERROR_CONTAINER,
)
def mod_button_text_style(
    color: ft.ColorValue = ft.Colors.PRIMARY,
    size: ft.OptionalNumber = 18,
    weight: ft.FontWeight = ft.FontWeight.NORMAL,
    font_family: str = DEFAULT_FONT_FAMILY,
    letter_spacing: ft.OptionalNumber = None
) -> ft.TextStyle:
    return ft.TextStyle(
        color=color,
        size=size,
        weight=weight,
        font_family=font_family,
        letter_spacing=letter_spacing
    )

# == Page Styles and Configs ==
def apply_default_page_config(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.random(), #TODO: Decide on a final color scheme
        font_family=DEFAULT_FONT_FAMILY,
    )
    page.theme_mode = load_theme_mode()
    
    page.scroll = ft.ScrollMode.ADAPTIVE
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
    page.window.height = 400


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
    animation_duration=100,
    icon_color=ft.Colors.ON_PRIMARY,
    icon_size=15,
    bgcolor=ft.Colors.PRIMARY,
    shape={
        ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(ft.border_radius.all(12)),
        ft.ControlState.PRESSED: ft.RoundedRectangleBorder(ft.border_radius.all(8)),
        ft.ControlState.FOCUSED: ft.RoundedRectangleBorder(ft.border_radius.all(10)),
    },
    side={
        ft.ControlState.DEFAULT: border_side(color=ft.Colors.PRIMARY),
        ft.ControlState.FOCUSED: border_side(color=ft.Colors.ON_TERTIARY),
    },
    overlay_color={
        ft.ControlState.DISABLED: ft.Colors.with_opacity(0.7, ft.Colors.SECONDARY),
        ft.ControlState.HOVERED: ft.Colors.with_opacity(0.5, ft.Colors.TERTIARY),
        ft.ControlState.PRESSED: ft.Colors.with_opacity(0.7, ft.Colors.TERTIARY),
        ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.5, ft.Colors.TERTIARY),
    },
    elevation={
        ft.ControlState.DEFAULT: 1,
        ft.ControlState.DISABLED: 0,
    },
    text_style={
        ft.ControlState.DEFAULT: mod_button_text_style(color=ft.Colors.PRIMARY),
        ft.ControlState.PRESSED: mod_button_text_style(color=ft.Colors.TERTIARY,weight=ft.FontWeight.BOLD),
        ft.ControlState.HOVERED: mod_button_text_style(color=ft.Colors.TERTIARY,weight=ft.FontWeight.W_500),
        ft.ControlState.FOCUSED: mod_button_text_style(color=ft.Colors.ON_TERTIARY,weight=ft.FontWeight.W_600),
    }
)

def build_action_button_style(
    primary: ft.ColorValue = ft.Colors.PRIMARY,
    on_primary: ft.ColorValue = ft.Colors.ON_PRIMARY,
    highlight: ft.ColorValue = ft.Colors.PRIMARY
) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        animation_duration=200,
        icon_color=on_primary,
        icon_size=15,
        bgcolor=primary,
        shape={
            ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(ft.border_radius.all(12)),
            ft.ControlState.PRESSED: ft.RoundedRectangleBorder(ft.border_radius.all(8))
        },
        side={
            ft.ControlState.DEFAULT: border_side(color=primary),
            ft.ControlState.FOCUSED: border_side(),
        },
        overlay_color={
            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.5, highlight),
            ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.3, highlight),
            ft.ControlState.PRESSED: ft.Colors.with_opacity(0.7, highlight),
        },
        elevation={
            ft.ControlState.DEFAULT: 1,
            ft.ControlState.DISABLED: 0
        }
    )