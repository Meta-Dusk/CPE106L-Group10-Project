import flet as ft

# from app.ui.components.containers import default_row
from app.ui.services.map_tile_utils import tile_to_url, latlon_to_tile_and_offset, tile_to_latlon
from app.ui.map_view.state import (
    zoom_level, center_tile_x, center_tile_y, center_lat, center_lon,
    pickup_pin, dropoff_pin, driver_marker, driver_icon_container
)
from app.ui.map_view.ui_elements import get_pin_icon, get_driver_icon
from app.ui.map_view.handlers import tile_click_handler


def cleanup_map_view():
    driver_icon_container[0] = None
    driver_marker[0] = None
    pickup_pin[0] = None
    dropoff_pin[0] = None
    
    # Clear anything else that won’t be reused

def compute_icon_offset(lat, lon, offset_x=16, offset_y=16):
    tile_x, tile_y, px, py = latlon_to_tile_and_offset(lat, lon, zoom_level[0])
    dx = (tile_x - center_tile_x[0] + 1) * 256
    dy = (tile_y - center_tile_y[0] + 1) * 256
    return dx + px - offset_x, dy + py - offset_y

def render_map(
    page: ft.Page,
    tile_stack: ft.Stack,
    pickup_lat_input: ft.TextField,
    pickup_lon_input: ft.TextField,
    dest_lat_input: ft.TextField,
    dest_lon_input: ft.TextField,
    pin_status: ft.Text
):
    tiles = []

    # Build 3x3 tile grid around center tile
    for dy in [-1, 0, 1]:
        row = []
        for dx in [-1, 0, 1]:
            tx = center_tile_x[0] - 1 + dx
            ty = center_tile_y[0] - 1 + dy
            url = tile_to_url(tx, ty, zoom_level[0])
            if not url:
                continue
            row.append(url)
        tiles.append(row)
        
    tile_stack.controls.clear()
    tile_rows = []

    for row_index in range(3):
        image_row = []
        for col_index in range(3):
            abs_tile_x = center_tile_x[0] - 1 + col_index
            abs_tile_y = center_tile_y[0] - 1 + row_index
            url = tile_to_url(abs_tile_x, abs_tile_y, zoom_level[0])

            tile_image = ft.Image(src=url, width=256, height=256, fit=ft.ImageFit.COVER)
            gesture = ft.GestureDetector(
                content=tile_image,
                on_tap_down=tile_click_handler(
                    center_tile_x[0], center_tile_y[0],
                    col_index, row_index,
                    page, tile_stack,
                    pickup_lat_input, pickup_lon_input,
                    dest_lat_input, dest_lon_input,
                    pin_status
                )
            )
            image_row.append(gesture)
        tile_rows.append(ft.Row(image_row, spacing=0))
        
    if driver_icon_container[0] and driver_icon_container[0] not in tile_stack.controls:
        tile_stack.controls.append(driver_icon_container[0])

    tile_stack.controls.append(ft.Column(tile_rows, spacing=0))

    def add_overlay_icon(lat, lon, icon, offset_x=20, offset_y=36):
        tile_x, tile_y, px, py = latlon_to_tile_and_offset(lat, lon, zoom_level[0])
        dx = (tile_x - center_tile_x[0] + 1) * 256
        dy = (tile_y - center_tile_y[0] + 1) * 256

        tile_stack.controls.append(
            ft.Container(
                content=icon,
                left=dx + px - offset_x,
                top=dy + py - offset_y,
                width=icon.size if hasattr(icon, "size") else 40,
                height=icon.size if hasattr(icon, "size") else 40
            )
        )
    
    PIN_OFFSETS = {
        "pickup": (20, 36),    # bottom-center of pin
        "dropoff": (10, 36),   # base of flag
        "driver": (16, 16)     # centered
    }
    
    # Pins
    if pickup_pin[0] is not None:
        ox, oy = PIN_OFFSETS["pickup"]
        add_overlay_icon(*pickup_pin[0], get_pin_icon("pickup"), offset_x=ox, offset_y=oy)

    if dropoff_pin[0] is not None:
        ox, oy = PIN_OFFSETS["dropoff"]
        add_overlay_icon(*dropoff_pin[0], get_pin_icon("dropoff"), offset_x=ox, offset_y=oy)

    # Create the driver icon container if it doesn't exist
    if driver_marker[0] is not None:
        lat, lon = driver_marker[0]
        dx, dy = compute_icon_offset(lat, lon, offset_x=16, offset_y=16)

        if driver_icon_container[0] is None:
            driver_icon_container[0] = ft.Container(
                content=get_driver_icon(),
                left=dx,
                top=dy,
                width=32,
                height=32
            )
            tile_stack.controls.append(driver_icon_container[0])
        else:
            # Just update its position
            driver_icon_container[0].left = dx
            driver_icon_container[0].top = dy
            driver_icon_container[0].update()
    
    # Update lat/lon center from tile center
    center_lat[0], center_lon[0] = tile_to_latlon(center_tile_x[0], center_tile_y[0], zoom_level[0])

    # Move driver icon to the top of stack (end of controls list)
    if driver_icon_container[0] in tile_stack.controls:
        tile_stack.controls.remove(driver_icon_container[0])
        tile_stack.controls.append(driver_icon_container[0])

    page.update()
