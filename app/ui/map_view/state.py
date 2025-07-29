import flet as ft
# Shared mutable state for map view

# Zoom level
zoom_level = [12]

# Metro Manila center
center_lat = [14.5995]
center_lon = [120.9842]

# Tile coordinates of center
center_tile_x = [0]
center_tile_y = [0]

# Pin mode state: "pickup" or "dropoff"
pin_mode = ["pickup"]

# Stored pin coordinates (lat, lon)
pickup_pin = [None]
dropoff_pin = [None]

# (lat, lon) position of moving driver
driver_marker = [None]
driver_icon_container = [None]  # Will hold the animated container

# Debug states
route_debug_overlay: list[ft.Control] = [None] # Holds debug markers/lines
show_debug_overlay: list[bool] = [True]        # Path overlay
cancel_simulation_flag: list[bool] = [False]   # Fast-forward simulation
current_debug_path: list[tuple[float, float]] = []