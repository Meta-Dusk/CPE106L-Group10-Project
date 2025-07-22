import flet as ft
from app.assets.images import ICON_PATH
from app.ui.theme_service import load_theme_mode
from dataclasses import dataclass
from enum import Enum


DEFAULT_FONT_FAMILY = "Roboto"
DEFAULT_INPUT_FIELD_WIDTH = 300
APP_NAME = "ATraS.App"


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
    

# == Text Styles ==
@dataclass
class TextStyle:
    font_family: str = DEFAULT_FONT_FAMILY
    size: ft.OptionalNumber = 18
    weight: ft.FontWeight = ft.FontWeight.NORMAL
    color: ft.ColorValue = ft.Colors.PRIMARY
    
class DefaultTextStyle(Enum):
    DEFAULT = TextStyle(color=ft.Colors.ON_SECONDARY)
    SUBTITLE = TextStyle(color=ft.Colors.ON_PRIMARY_CONTAINER, size=20)
    TITLE = TextStyle(weight=ft.FontWeight.BOLD, size=25)
    ERROR = TextStyle(color=ft.Colors.ON_ERROR_CONTAINER)
    LABEL = TextStyle(size=18)
    HINT = TextStyle(size=16, color=ft.Colors.SECONDARY)
    
def build_text_style(style: TextStyle) -> ft.TextStyle:
    return ft.TextStyle(
        font_family=style.font_family,
        size=style.size,
        weight=style.weight,
        color=style.color
    )


# == Input Field Styles ==
@dataclass
class InputFieldConfig:
    label: ft.OptionalString = None
    label_style: ft.TextStyle | None = None
    width: int = 400
    height: int = 70
    auto_focus: bool = False
    password: bool = False
    can_reveal_password: bool = False
    selection_color: ft.ColorValue = ft.Colors.RED
    bg_color: ft.ColorValue = ft.Colors.PRIMARY_CONTAINER
    color: ft.ColorValue = ft.Colors.ON_PRIMARY_CONTAINER
    hint_text: ft.OptionalString = None
    hint_style: ft.TextStyle = None
    border_radius: ft.BorderRadiusValue = None
    adaptive: bool = True
    size_constraints: ft.BoxConstraints = None
    expand: bool = True
    
    def __post_init__(self):
        if self.hint_text is None and self.label is not None:
            self.hint_text = f"Please enter your {self.label.lower()} here."
        if self.hint_style is None:
            self.hint_style = build_text_style(DefaultTextStyle.HINT.value)
        if self.border_radius is None:
            self.border_radius = ft.border_radius.all(10)
        if self.label_style is None:
            self.label_style = build_text_style(DefaultTextStyle.LABEL.value)
        if self.size_constraints is None:
            self.size_constraints = ft.BoxConstraints(
                min_width=self.width,
                min_height=self.height,
                max_width=self.width * 1.5,
                max_height=self.height * 1.5
            )
    
class DefaultInputFieldType(Enum):
    USERNAME = InputFieldConfig(
        label="Username",
        auto_focus=True,
    )
    PASSWORD = InputFieldConfig(
        label="Password",
        password=True,
        can_reveal_password=True
    )
    URI = InputFieldConfig(
        label="MongoDB URI",
        hint_text="Input the full connection string here",
        width=500,
        password=True,
        can_reveal_password=True,
        auto_focus=True
    )
    HOST = InputFieldConfig(
        label="Host",
        hint_text="i.e. cluster.mongodb.net"
    )
    

# == Page Styles and Configs ==
def apply_default_page_config(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.DEEP_ORANGE,
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
    
def apply_setup_page_config(page: ft.Page, alt: bool = False):
    static_page_config(page)
    default_page_border(page)
    page.title = f"{APP_NAME} | Setup"
    page.window.width = 600
    if alt:
        page.window.height = 550
    else:
        page.window.height = 380


# == Button Styles
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
    
default_action_button_style = ft.ButtonStyle(
    animation_duration=100,
    icon_color=ft.Colors.ON_PRIMARY,
    icon_size=15,
    color=ft.Colors.ON_PRIMARY,
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
        ft.ControlState.DISABLED: mod_button_text_style(color=ft.Colors.SECONDARY),
    }
)

def build_action_button_style(
    primary: ft.ColorValue = ft.Colors.PRIMARY,
    on_primary: ft.ColorValue = ft.Colors.ON_PRIMARY,
    primary_highlight: ft.ColorValue = ft.Colors.TERTIARY,
    seconday_highlight: ft.ColorValue = ft.Colors.ON_TERTIARY,
    text_size: ft.OptionalNumber = 18
) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        animation_duration=100,
        icon_color=on_primary,
        icon_size=15,
        color=on_primary,
        bgcolor=primary,
        shape={
            ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(ft.border_radius.all(12)),
            ft.ControlState.PRESSED: ft.RoundedRectangleBorder(ft.border_radius.all(8)),
            ft.ControlState.FOCUSED: ft.RoundedRectangleBorder(ft.border_radius.all(10)),
        },
        side={
            ft.ControlState.DEFAULT: border_side(primary),
            ft.ControlState.FOCUSED: border_side(seconday_highlight),
        },
        overlay_color={
            ft.ControlState.DISABLED: ft.Colors.with_opacity(0.7, ft.Colors.SECONDARY),
            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.5, primary_highlight),
            ft.ControlState.PRESSED: ft.Colors.with_opacity(0.7, primary_highlight),
            ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.5, primary_highlight),
        },
        elevation={
            ft.ControlState.DEFAULT: 1,
            ft.ControlState.DISABLED: 0,
        },
        text_style={
            ft.ControlState.DEFAULT: mod_button_text_style(primary, size=text_size),
            ft.ControlState.PRESSED: mod_button_text_style(primary_highlight, weight=ft.FontWeight.BOLD, size=text_size),
            ft.ControlState.HOVERED: mod_button_text_style(primary_highlight, weight=ft.FontWeight.W_500, size=text_size),
            ft.ControlState.FOCUSED: mod_button_text_style(seconday_highlight, weight=ft.FontWeight.W_600, size=text_size),
        }
    )