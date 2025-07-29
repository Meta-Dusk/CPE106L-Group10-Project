from app.ui.services.map_tile_utils import latlon_to_tile, tile_to_latlon
from app.ui.map_view import state, render


def zoom_in(page, tile_stack, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status):
    if state.zoom_level[0] < 19:
        state.center_lat[0], state.center_lon[0] = tile_to_latlon(
            state.center_tile_x[0], state.center_tile_y[0], state.zoom_level[0]
        )
        state.zoom_level[0] += 1
        state.center_tile_x[0], state.center_tile_y[0] = latlon_to_tile(
            state.center_lat[0], state.center_lon[0], state.zoom_level[0]
        )
        render.render_map(
            page, tile_stack,
            pickup_lat_input, pickup_lon_input,
            dest_lat_input, dest_lon_input,
            pin_status
        )

def zoom_out(page, tile_stack, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status):
    if state.zoom_level[0] > 1:
        state.center_lat[0], state.center_lon[0] = tile_to_latlon(
            state.center_tile_x[0], state.center_tile_y[0], state.zoom_level[0]
        )
        state.zoom_level[0] -= 1
        state.center_tile_x[0], state.center_tile_y[0] = latlon_to_tile(
            state.center_lat[0], state.center_lon[0], state.zoom_level[0]
        )
        render.render_map(
            page, tile_stack,
            pickup_lat_input, pickup_lon_input,
            dest_lat_input, dest_lon_input,
            pin_status
        )

def pan_map(dx, dy, page, tile_stack, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status):
    state.center_tile_x[0] += dx
    state.center_tile_y[0] += dy
    render.render_map(
        page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )
