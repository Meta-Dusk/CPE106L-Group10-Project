import asyncio
import flet as ft

from app.ui.services.booking_sim import simulate_booking
from app.ui.services.map_tile_utils import latlon_to_tile
from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton
from app.ui.components.containers import div, default_row, spaced_buttons, preset_container, default_column
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, theme_toggle_button, mod_toggle_theme, preset_exit_button
)
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.routing.route_data import PageRoute

from app.ui.map_view.render import render_map
from app.ui.map_view.state import (
    pin_mode, center_tile_x, center_tile_y, center_lon, center_lat, zoom_level)
from app.ui.map_view.ui_elements import (
    get_zoom_controls, get_pan_controls, get_booking_controls,
    get_pin_controls, get_image_grid_container
)


def handle_mapview(page: ft.Page, _):
    # ─── UI Elements ───────────────────────────────
    title = default_text(DefaultTextStyle.TITLE, "Map View (Metro Manila)")

    logo = set_logo()
    toggleable_logo = container_setup(logo)

    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, theme_toggle],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )

    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    logout_btn = preset_logout_button(page)

    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=lambda e: page.go(PageRoute.DASHBOARD.value)
    )
    exit_btn = preset_exit_button(page)

    control_buttons = default_row([logout_btn, back_btn])
    top_row = spaced_buttons([exit_btn], [theme_toggle])
    title_container = preset_container(title, ft.Colors.PRIMARY_CONTAINER)
    
    # ─── Inputs & Controls ─────────────────────────
    pickup_lat_input = ft.TextField(label="Pickup Latitude", width=200)
    pickup_lon_input = ft.TextField(label="Pickup Longitude", width=200)
    dest_lat_input = ft.TextField(label="Destination Latitude", width=200)
    dest_lon_input = ft.TextField(label="Destination Longitude", width=200)
    booking_status = ft.Text(value="No booking in progress...", size=14)
    pin_mode_text = ft.Text(value="Current mode: Set Pickup", size=12)
    pin_status_text = ft.Text(value="No pins set yet.", size=12)
    image_grid = ft.Column(spacing=0)

    # ─── Pin Mode Handlers ─────────────────────────
    def update_pin_mode_label():
        pin_mode_text.value = f"Current mode: Set {'Pickup' if pin_mode[0] == 'pickup' else 'Drop-off'}"
        page.update()

    set_pickup = lambda e: (pin_mode.__setitem__(0, "pickup"), update_pin_mode_label())
    set_dropoff = lambda e: (pin_mode.__setitem__(0, "dropoff"), update_pin_mode_label())

    # ─── Booking Sim Logic ─────────────────────────
    async def handle_booking(e):
        try:
            pickup = (float(pickup_lat_input.value), float(pickup_lon_input.value))
            dest = (float(dest_lat_input.value), float(dest_lon_input.value))
            await simulate_booking(
                pickup, dest,
                lambda msg: (booking_status.__setattr__('value', msg), page.update()),
                page, image_grid,
                pickup_lat_input, pickup_lon_input,
                dest_lat_input, dest_lon_input,
                pin_status_text
            )
        except Exception as ex:
            booking_status.value = f"Error: {ex}"
            page.update()

    # ─── Build Modular UI ──────────────────────────
    zoom_controls = get_zoom_controls(
        page, image_grid,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status_text
    )
    pan_controls = get_pan_controls(
        page, image_grid,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status_text
    )
    pin_controls = get_pin_controls(set_pickup, set_dropoff, pin_mode_text, pin_status_text)
    booking_controls = get_booking_controls(
        lambda e: asyncio.run(handle_booking(e)),
        pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, booking_status
    )
    map_container = get_image_grid_container(image_grid)

    # ─── Layout Composition ────────────────────────
    map_view_section = default_column([
        pin_controls,
        booking_controls,
        spaced_buttons([zoom_controls], [pan_controls]),
        map_container
    ])

    form = [
        top_row,
        toggleable_logo,
        div(),
        title_container,
        div(),
        preset_container(map_view_section),
        div(),
        control_buttons
    ]
    
    # Sync tile state from initial lat/lon
    center_tile_x[0], center_tile_y[0] = latlon_to_tile(center_lat[0], center_lon[0], zoom_level[0])

    # ─── Final Rendering ───────────────────────────
    render_page(page, form)
    render_map(page, image_grid, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status_text)