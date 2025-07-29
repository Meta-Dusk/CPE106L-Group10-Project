import flet as ft

from app.assets.audio_manager import audio, SFX
from app.ui.components.buttons import default_action_button, default_action_button_style
from app.ui.components.containers import default_column, default_row, preset_container
from app.ui.styles import build_text_style, DefaultTextStyle
from app.ui.map_view import controller
from enum import Enum


def get_zoom_controls(
    page, tile_stack,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    pin_status
):
    zoom_in_btn = default_action_button(
        text="Zoom In",
        icon=ft.Icons.ZOOM_IN_MAP,
        tooltip="Zoom in the map view",
        on_click=lambda e: controller.zoom_in(
            page, tile_stack,
            pickup_lat_input, pickup_lon_input,
            dest_lat_input, dest_lon_input,
            pin_status
        ),
        width=200
    )
    zoom_out_btn = default_action_button(
        text="Zoom Out",
        icon=ft.Icons.ZOOM_OUT_MAP,
        tooltip="Zoom out the map view",
        on_click=lambda e: controller.zoom_out(
            page, tile_stack,
            pickup_lat_input, pickup_lon_input,
            dest_lat_input, dest_lon_input,
            pin_status
        ),
        width=200
    )
    return preset_container(
        content=default_row([zoom_in_btn, zoom_out_btn]),
        bgcolor=ft.Colors.INVERSE_PRIMARY
    )

class Pan(Enum):
    UP = 0, -1
    LEFT = -1, 0
    DOWN = 0, 1
    RIGHT = 1, 0

def build_pan_button(
    direction: Pan,
    page, tile_stack,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    pin_status
) -> ft.IconButton:
    icon_enum: ft.IconValue = getattr(ft.Icons, f"KEYBOARD_ARROW_{direction.name}")
    generated_tooltip = f"Pan {direction.name.lower().capitalize()}"
    dx, dy = direction.value

    generated_callback = lambda e: controller.pan_map(
        dx, dy, page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
    
    return ft.IconButton(
        icon=icon_enum,
        icon_size=50,
        tooltip=generated_tooltip,
        style=default_action_button_style,
        on_click=generated_callback
    )

def get_pan_controls(
    page, tile_stack,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    pin_status
) -> ft.Container:
    pan_up_btn = build_pan_button(
        Pan.UP, page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
    pan_left_btn = build_pan_button(
        Pan.LEFT, page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
    pan_down_btn = build_pan_button(
        Pan.DOWN, page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
    pan_right_btn = build_pan_button(
        Pan.RIGHT, page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
    bottom_row = default_row([pan_left_btn, pan_down_btn, pan_right_btn])
    return preset_container(
        content=default_column([pan_up_btn, bottom_row]),
        bgcolor=ft.Colors.INVERSE_PRIMARY
    )


def get_booking_controls(
    cancel_callback, book_callback,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    booking_status_text
):
    cancel_sim_btn = default_action_button(
        text="Cancel Simulation",
        icon=ft.Icons.CANCEL,
        tooltip="Stop current simulation",
        on_click=cancel_callback,
        width=200
    )
    booking_btn = default_action_button(
        text="Simulate Booking",
        icon=ft.Icons.LOCAL_TAXI,
        tooltip="Simulate ride booking",
        on_click=book_callback,
        width=200
    )
    latlon_inputs = default_row([
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input
    ])
    return preset_container(
        content=default_column([
            latlon_inputs,
            default_row([booking_btn, cancel_sim_btn]),
            booking_status_text
        ]),
        bgcolor=ft.Colors.INVERSE_PRIMARY
    )


def get_pin_controls(set_pickup, set_dropoff, pin_mode_text, pin_status_text):
    set_pickup_btn = default_action_button(
        text="Set Pickup",
        icon=ft.Icons.LOCATION_ON,
        tooltip="Click map to set pickup location",
        on_click=set_pickup,
        width=200
    )

    set_dropoff_btn = default_action_button(
        text="Set Drop-off",
        icon=ft.Icons.FLAG,
        tooltip="Click map to set destination",
        on_click=set_dropoff,
        width=200
    )

    return default_column([
        pin_mode_text,
        default_row([set_pickup_btn, set_dropoff_btn]),
        pin_status_text
    ])


def get_tile_stack_container(tile_stack: ft.Stack):
    return ft.Container(
        content=tile_stack,
        # width=768, height=768,
        bgcolor=ft.Colors.INVERSE_PRIMARY, border_radius=20,
        padding=10, alignment=ft.alignment.center, expand=True
    )


def get_pin_icon(pin_type: str) -> ft.Icon:
    return ft.Icon(
        name=ft.Icons.LOCATION_ON if pin_type == "pickup" else ft.Icons.FLAG,
        color=ft.Colors.GREEN if pin_type == "pickup" else ft.Colors.RED,
        size=40, blend_mode=ft.BlendMode.DARKEN
    )

def get_driver_icon():
    return ft.Icon(
        name=ft.Icons.DIRECTIONS_CAR,
        color=ft.Colors.BLUE,
        size=32
    )

def latlon_text_field(
    label: str,
    width: int = 400,
    height: int = 50
) -> ft.TextField:
    generate_hint_text = f"Enter {label} here"
    
    return ft.TextField(
        label=label,
        width=width,
        height=height,
        selection_color=ft.Colors.INVERSE_PRIMARY,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        color=ft.Colors.ON_PRIMARY_CONTAINER,
        expand=True,
        adaptive=True,
        hint_text=generate_hint_text,
        hint_style=build_text_style(DefaultTextStyle.HINT.value),
        label_style=build_text_style(DefaultTextStyle.LABEL.value),
        border_radius=ft.border_radius.all(10),
        size_constraints=ft.BoxConstraints(
            min_width=width,
            min_height=height,
            max_width=width * 1.5,
            max_height=height * 1.5
        )
    )

def get_debug_controls(toggle_debug_callback):
    return default_action_button(
        text="Toggle Debug Overlay",
        icon=ft.Icons.BUG_REPORT,
        tooltip="Show or hide route debug overlay",
        on_click=toggle_debug_callback,
        width=220
    )
