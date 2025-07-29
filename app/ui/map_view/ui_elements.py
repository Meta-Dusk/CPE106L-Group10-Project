import flet as ft

from app.ui.components.buttons import default_action_button, default_action_button_style
from app.ui.components.containers import default_column, default_row, preset_container
from app.ui.components.text import default_text
from app.ui.map_view import controller


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


def get_pan_controls(
    page, tile_stack,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    pin_status
):
    return preset_container(
        content=default_column([
            ft.IconButton(
                icon=ft.Icons.KEYBOARD_ARROW_UP,
                icon_size=50,
                tooltip="Pan Up",
                style=default_action_button_style,
                on_click=lambda e: controller.pan_map(
                    0, -1, page, tile_stack,
                    pickup_lat_input, pickup_lon_input,
                    dest_lat_input, dest_lon_input,
                    pin_status
                )
            ),
            default_row([
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                    icon_size=50,
                    tooltip="Pan Left",
                    style=default_action_button_style,
                    on_click=lambda e: controller.pan_map(
                        -1, 0, page, tile_stack,
                        pickup_lat_input, pickup_lon_input,
                        dest_lat_input, dest_lon_input,
                        pin_status
                    )
                ),
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                    icon_size=50,
                    tooltip="Pan Down",
                    style=default_action_button_style,
                    on_click=lambda e: controller.pan_map(
                        0, 1, page, tile_stack,
                        pickup_lat_input, pickup_lon_input,
                        dest_lat_input, dest_lon_input,
                        pin_status
                    )
                ),
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                    icon_size=50,
                    tooltip="Pan Right",
                    style=default_action_button_style,
                    on_click=lambda e: controller.pan_map(
                        1, 0, page, tile_stack,
                        pickup_lat_input, pickup_lon_input,
                        dest_lat_input, dest_lon_input,
                        pin_status
                    )
                ),
            ])
        ]),
        bgcolor=ft.Colors.INVERSE_PRIMARY
    )


def get_booking_controls(book_callback, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, booking_status_text):
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
            booking_btn,
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
