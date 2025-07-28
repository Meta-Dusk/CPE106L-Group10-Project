import flet as ft

# from app.ui.components.containers import default_row
from app.ui.services.map_tile_utils import tile_to_url, latlon_to_tile_and_offset, tile_to_latlon
from app.ui.map_view.state import (
    zoom_level, center_tile_x, center_tile_y, center_lat, center_lon,
    pickup_pin, dropoff_pin, driver_marker
)
from app.ui.map_view.ui_elements import get_pin_icon, get_driver_icon
from app.ui.map_view.handlers import tile_click_handler


def render_map(
    page: ft.Page,
    image_grid: ft.Column,
    pickup_lat_input: ft.TextField,
    pickup_lon_input: ft.TextField,
    dest_lat_input: ft.TextField,
    dest_lon_input: ft.TextField,
    pin_status: ft.Text
):
    image_grid.controls.clear()
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

    def place_icon_for_marker(lat, lon, icon, tile_x, tile_y):
        marker_tile_x, marker_tile_y, pixel_x, pixel_y = latlon_to_tile_and_offset(lat, lon, zoom_level[0])
        if marker_tile_x == tile_x and marker_tile_y == tile_y:
            layers.append(
                ft.Container(
                    content=icon,
                    left=pixel_x - 16,  # adjust based on icon size
                    top=pixel_y - 16,
                )
            )
    
    for row_index, row in enumerate(tiles):
        image_row = []
        for col_index, url in enumerate(row):
            abs_tile_x = center_tile_x[0] - 1 + col_index
            abs_tile_y = center_tile_y[0] - 1 + row_index
            # print(f"Tile ({abs_tile_x}, {abs_tile_y}, zoom {zoom_level[0]}) -> {url}")
            # print(f"Zoom: {zoom_level[0]}, Center Tile: ({center_tile_x[0]}, {center_tile_y[0]})")

            layers = [
                ft.Container(
                    content=ft.Image(src=url, width=256, height=256, fit=ft.ImageFit.COVER),
                    # border=ft.border.all(1, ft.Colors.BLACK),
                    alignment=ft.alignment.center,
                ),
                # ft.Text(f"{abs_tile_x},{abs_tile_y}", size=10, color=ft.Colors.WHITE)
            ]

            def place_icon_for_pin(pin, pin_type):
                if pin[0] is not None:
                    lat, lon = pin[0]
                    pin_tile_x, pin_tile_y, pixel_x, pixel_y = latlon_to_tile_and_offset(lat, lon, zoom_level[0])
                    if pin_tile_x == abs_tile_x and pin_tile_y == abs_tile_y:
                        if pin_type == "pickup":
                            offset_x, offset_y = 20, 36  # tip of pin is bottom-center
                        else:  # drop-off
                            offset_x, offset_y = 10, 36  # adjust for flag visual anchor
                
                        layers.append(
                            ft.Container(
                                content=get_pin_icon(pin_type),
                                left=pixel_x - offset_x,
                                top=pixel_y - offset_y
                            )
                        )
                        layers.append(ft.Container(
                            left=pixel_x - 2,
                            top=pixel_y - 2,
                            width=4,
                            height=4,
                            bgcolor=ft.Colors.BLACK,
                            border_radius=2
                        ))
                        
            if driver_marker[0] is not None:
                lat, lon = driver_marker[0]
                place_icon_for_marker(lat, lon, get_driver_icon(), abs_tile_x, abs_tile_y)

            place_icon_for_pin(pickup_pin, "pickup")
            place_icon_for_pin(dropoff_pin, "dropoff")

            tile_stack = ft.Stack(
                controls=layers,
                width=256,
                height=256,
                clip_behavior=ft.ClipBehavior.NONE
            )
            # img = ft.Image(src=url, width=256, height=256, fit=ft.ImageFit.COVER)
            # print(f"Created image: {url}")
            # layers = [img]
            gesture_tile = ft.GestureDetector(
                content=tile_stack,
                on_tap_down=tile_click_handler(
                    center_tile_x[0], center_tile_y[0],
                    col_index, row_index,
                    page, image_grid,
                    pickup_lat_input, pickup_lon_input,
                    dest_lat_input, dest_lon_input,
                    pin_status
                )
            )
            image_row.append(gesture_tile)

        image_grid.controls.append(ft.Row(controls=image_row, spacing=0))

    # Update lat/lon center from tile center
    center_lat[0], center_lon[0] = tile_to_latlon(center_tile_x[0], center_tile_y[0], zoom_level[0])
    page.update()
