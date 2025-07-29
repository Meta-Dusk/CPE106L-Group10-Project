import math
import flet as ft

from app.ui.services.map_tile_utils import tile_to_url, latlon_to_tile_and_offset, tile_to_latlon
from app.ui.map_view import state
from app.ui.map_view.ui_elements import get_pin_icon, get_driver_icon
from app.ui.map_view.handlers import tile_click_handler
from geopy.distance import geodesic


def cleanup_map_view():
    state.driver_icon_container[0] = None
    state.driver_marker[0] = None
    state.pickup_pin[0] = None
    state.dropoff_pin[0] = None
    
    # Clear anything else that won’t be reused

def compute_icon_offset(lat, lon, offset_x=16, offset_y=16):
    tile_x, tile_y, px, py = latlon_to_tile_and_offset(lat, lon, state.zoom_level[0])
    dx = (tile_x - state.center_tile_x[0] + 1) * 256
    dy = (tile_y - state.center_tile_y[0] + 1) * 256
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
            tx = state.center_tile_x[0] - 1 + dx
            ty = state.center_tile_y[0] - 1 + dy
            url = tile_to_url(tx, ty, state.zoom_level[0])
            if not url:
                continue
            row.append(url)
        tiles.append(row)
        
    tile_stack.controls.clear()
    tile_rows = []

    for row_index in range(3):
        image_row = []
        for col_index in range(3):
            abs_tile_x = state.center_tile_x[0] - 1 + col_index
            abs_tile_y = state.center_tile_y[0] - 1 + row_index
            url = tile_to_url(abs_tile_x, abs_tile_y, state.zoom_level[0])

            tile_image = ft.Image(src=url, width=256, height=256, fit=ft.ImageFit.COVER)
            gesture = ft.GestureDetector(
                content=tile_image,
                on_tap_down=tile_click_handler(
                    state.center_tile_x[0], state.center_tile_y[0],
                    col_index, row_index,
                    page, tile_stack,
                    pickup_lat_input, pickup_lon_input,
                    dest_lat_input, dest_lon_input,
                    pin_status
                )
            )
            image_row.append(gesture)
        tile_rows.append(ft.Row(image_row, spacing=0))
        
    if state.driver_icon_container[0] and state.driver_icon_container[0] not in tile_stack.controls:
        tile_stack.controls.append(state.driver_icon_container[0])

    tile_stack.controls.append(ft.Column(tile_rows, spacing=0))

    def add_overlay_icon(lat, lon, icon, offset_x=20, offset_y=36):
        tile_x, tile_y, px, py = latlon_to_tile_and_offset(lat, lon, state.zoom_level[0])
        dx = (tile_x - state.center_tile_x[0] + 1) * 256
        dy = (tile_y - state.center_tile_y[0] + 1) * 256

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
    if state.pickup_pin[0] is not None:
        ox, oy = PIN_OFFSETS["pickup"]
        add_overlay_icon(*state.pickup_pin[0], get_pin_icon("pickup"), offset_x=ox, offset_y=oy)

    if state.dropoff_pin[0] is not None:
        ox, oy = PIN_OFFSETS["dropoff"]
        add_overlay_icon(*state.dropoff_pin[0], get_pin_icon("dropoff"), offset_x=ox, offset_y=oy)

    # Create the driver icon container if it doesn't exist
    if state.driver_marker[0] is not None:
        lat, lon = state.driver_marker[0]
        dx, dy = compute_icon_offset(lat, lon, offset_x=16, offset_y=16)

        if state.driver_icon_container[0] is None:
            state.driver_icon_container[0] = ft.Container(
                content=get_driver_icon(),
                left=dx,
                top=dy,
                width=32,
                height=32
            )
            tile_stack.controls.append(state.driver_icon_container[0])
        else:
            # Just update its position
            state.driver_icon_container[0].left = dx
            state.driver_icon_container[0].top = dy
            state.driver_icon_container[0].update()
    
    # Update lat/lon center from tile center
    state.center_lat[0], state.center_lon[0] = tile_to_latlon(state.center_tile_x[0], state.center_tile_y[0], state.zoom_level[0])

    # Move driver icon to the top of stack (end of controls list)
    if state.driver_icon_container[0] in tile_stack.controls:
        tile_stack.controls.remove(state.driver_icon_container[0])
        tile_stack.controls.append(state.driver_icon_container[0])
    
    # 🧭 Re-render debug overlay (if enabled)
    if state.show_debug_overlay[0] and state.current_debug_path:
        render_route_debug_overlay(page, tile_stack, state.current_debug_path)

    page.update()


def compute_raw_offset(lat, lon, zoom):
    """Get exact (x, y) pixel offset on tile stack without centering adjustment."""
    _, _, x_px, y_px = latlon_to_tile_and_offset(lat, lon, zoom)
    return x_px, y_px

def render_route_debug_overlay(page, tile_stack, path: list[tuple[float, float]]):
    if not state.show_debug_overlay[0]:
        return

    if state.route_debug_overlay[0] is not None:
        tile_stack.controls = [c for c in tile_stack.controls if c not in state.route_debug_overlay[0]]

    overlay_controls = []

    for i in range(1, len(path)):
        lat1, lon1 = path[i - 1]
        lat2, lon2 = path[i]

        def get_map_coords(lat, lon):
            tile_x, tile_y, px, py = latlon_to_tile_and_offset(lat, lon, state.zoom_level[0])
            dx = (tile_x - state.center_tile_x[0] + 1) * 256
            dy = (tile_y - state.center_tile_y[0] + 1) * 256
            return dx + px, dy + py

        x1, y1 = get_map_coords(lat1, lon1)
        x2, y2 = get_map_coords(lat2, lon2)

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        line = ft.Container(
            left=x1,
            top=y1,
            width=length,
            height=3,
            bgcolor=ft.Colors.ORANGE,
            border_radius=1.5,
            rotate=ft.Rotate(angle, alignment=ft.alignment.center_left),
            animate_rotation=ft.Animation(0)
        )

        tile_stack.controls.append(line)
        overlay_controls.append(line)

    # Add route info label
    total_km = sum(geodesic(path[i - 1], path[i]).km for i in range(1, len(path)))
    avg_speed_kmh = 40
    est_minutes = (total_km / avg_speed_kmh) * 60

    label = ft.Container(
        left=16,
        top=16,
        padding=8,
        bgcolor=ft.Colors.ORANGE_100,
        border_radius=8,
        content=ft.Text(
            value=f"{total_km:.2f} km | ~{est_minutes:.0f} min",
            color=ft.Colors.BLACK,
            size=12,
            weight=ft.FontWeight.W_500
        )
    )

    tile_stack.controls.append(label)
    overlay_controls.append(label)

    state.route_debug_overlay[0] = overlay_controls
    page.update()