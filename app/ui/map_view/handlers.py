import asyncio
import flet as ft

from app.ui.services.geocode_api import reverse_geocode
from app.ui.services.map_tile_utils import tile_pixel_to_latlon
from app.ui.map_view import state, render


async def resolve_location_name(lat: float, lon: float, text_element: ft.Text, pin_type: str, page: ft.Page):
    text_element.value = "Looking up location..."
    page.update()

    try:
        name = await reverse_geocode(lat, lon)
        text_element.value = f"{pin_type.capitalize()} set at: {name}"
    except Exception as ex:
        text_element.value = f"Error resolving location: {ex}"

    page.update()


def tile_click_handler(
    tile_x, tile_y, offset_x, offset_y,
    page: ft.Page,
    tile_stack: ft.Stack,
    pickup_lat_input: ft.TextField, pickup_lon_input: ft.TextField,
    dest_lat_input: ft.TextField, dest_lon_input: ft.TextField,
    pin_status: ft.Text
):
    def handler(e: ft.TapEvent):
        try:
            px, py = e.local_x, e.local_y

            top_left_tile_x = state.center_tile_x[0] - 1
            top_left_tile_y = state.center_tile_y[0] - 1

            abs_tile_x = top_left_tile_x + offset_x
            abs_tile_y = top_left_tile_y + offset_y

            lon, lat = tile_pixel_to_latlon(abs_tile_x, abs_tile_y, px, py, state.zoom_level[0])
            # print(f"[DEBUG] Tap @ px={px}, py={py} on tile {abs_tile_x}, {abs_tile_y}")

            if state.pin_mode[0] == "pickup":
                state.pickup_pin[0] = (lat, lon)
                pickup_lat_input.value = f"{lat:.6f}"
                pickup_lon_input.value = f"{lon:.6f}"
                pickup_lat_input.update()
                pickup_lon_input.update()
                asyncio.run(resolve_location_name(lat, lon, pin_status, "pickup", page))
            else:
                state.dropoff_pin[0] = (lat, lon)
                dest_lat_input.value = f"{lat:.6f}"
                dest_lon_input.value = f"{lon:.6f}"
                dest_lat_input.update()
                dest_lon_input.update()
                asyncio.run(resolve_location_name(lat, lon, pin_status, "drop-off", page))

            render.render_map(
                page, tile_stack,
                pickup_lat_input, pickup_lon_input,
                dest_lat_input, dest_lon_input,
                pin_status
            )
        except Exception as ex:
            pin_status.value = f"Click error: {ex}"
            page.update()

    return handler
