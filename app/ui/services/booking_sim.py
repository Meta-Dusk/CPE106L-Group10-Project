import random
import asyncio
import math

import flet as ft

from geopy.distance import geodesic
from app.ui.map_view import state, render
from app.ui.services.map_tile_utils import latlon_to_tile_and_offset
from app.ui.map_view.ui_elements import get_driver_icon


def safe_update_page(page):
    try:
        page.update()
    except Exception as e:
        print(f"[ERROR] Page update failed: {e}")

def update_driver_position(lat, lon):
    container = state.driver_icon_container[0]

    if container is None:
        print("[WARN] Tried to update driver icon position before it was created.")
        return

    dx, dy = render.compute_icon_offset(lat, lon, offset_x=16, offset_y=16)
    container.left = dx
    container.top = dy

    # ✅ Only update if still mounted
    if container.page is not None:
        container.update()
    else:
        print("[WARN] Driver icon no longer mounted on page; skipping update.")

def get_random_wait_time(min_seconds=2, max_seconds=5):
    return random.uniform(min_seconds, max_seconds)

def get_random_driver_location(pickup_lat, pickup_lon, max_distance_m=1000):
    """Generate a random driver location within a distance of pickup."""
    bearing = random.uniform(0, 360)
    distance_km = random.uniform(0.1, max_distance_m / 1000)

    lat_shift = distance_km / 111  # ~1° ≈ 111km
    lon_shift = lat_shift / abs(math.cos(math.radians(pickup_lat)))

    delta_lat = lat_shift * math.cos(math.radians(bearing))
    delta_lon = lon_shift * math.sin(math.radians(bearing))

    return pickup_lat + delta_lat, pickup_lon + delta_lon

def ease_in_out(t):
    """Cubic ease-in-out: accelerates and decelerates smoothly"""
    return 3 * t**2 - 2 * t**3

async def simulate_booking(
    pickup, destination, status_callback,
    page, tile_stack,
    pickup_lat_input, pickup_lon_input,
    dest_lat_input, dest_lon_input,
    pin_status
):
    """
    Simulate full ride booking process:
    1. Booking & driver assignment
    2. Driver approaching
    3. Pickup
    4. En route to destination
    5. Arrival
    """

    status_callback("Booking in progress...")

    # === Step 1: Wait for driver match ===
    wait_time = get_random_wait_time()
    status_callback(f"Searching for driver... ETA: {wait_time:.1f}s")
    await asyncio.sleep(wait_time)

    driver_location = get_random_driver_location(*pickup)
    driver_distance = geodesic(pickup, driver_location).km
    status_callback(f"Driver found! {driver_distance:.2f} km away")

    state.driver_marker[0] = driver_location
    tile_stack.controls = [c for c in tile_stack.controls if c is not None]
    page.update()
    
    render.render_map(
        page, tile_stack, pickup_lat_input, pickup_lon_input, dest_lat_input,
        dest_lon_input, pin_status
    )
    
    if state.driver_icon_container[0] is None:
        dx, dy = render.compute_icon_offset(driver_location[0], driver_location[1], offset_x=16, offset_y=16)

        container = ft.Container(
            content=get_driver_icon(),
            left=dx,
            top=dy,
            width=32,
            height=32
        )
        state.driver_icon_container[0] = container
        
        tile_stack.controls = [c for c in tile_stack.controls if c is not None]
        tile_stack.controls.append(container)
        safe_update_page(page)
        update_driver_position(driver_location[0], driver_location[1])
        
    update_driver_position(driver_location[0], driver_location[1])
    
    # === Step 2: Simulate driver approaching pickup ===
    duration = 3.0  # seconds
    fps = 60
    steps = int(duration * fps)

    for i in range(steps):
        t = (i + 1) / steps
        pct = ease_in_out(t)

        lat = driver_location[0] + (pickup[0] - driver_location[0]) * pct
        lon = driver_location[1] + (pickup[1] - driver_location[1]) * pct

        state.driver_marker[0] = (lat, lon)
        update_driver_position(lat, lon)

        dist = geodesic((lat, lon), pickup).km
        status_callback(f"Driver approaching... {dist * 1000:.0f}m away")

        await asyncio.sleep(1 / fps)

    # === Step 3: Picked up ===
    status_callback("Driver has arrived. Picking you up...")
    await asyncio.sleep(2)

    # === Step 4: En route to destination ===
    duration = 5.0  # longer trip
    steps = int(duration * fps)

    for i in range(steps):
        t = (i + 1) / steps
        pct = ease_in_out(t)

        lat = pickup[0] + (destination[0] - pickup[0]) * pct
        lon = pickup[1] + (destination[1] - pickup[1]) * pct

        state.driver_marker[0] = (lat, lon)
        update_driver_position(lat, lon)

        dist_remaining = geodesic((lat, lon), destination).km
        status_callback(f"En route... {dist_remaining:.2f} km remaining")

        await asyncio.sleep(1 / fps)

    # === Step 5: Arrived ===
    state.driver_marker[0] = (lat, lon)
    update_driver_position(lat, lon)

    status_callback("Arrived at destination. Thank you for riding! 🚗")
    return destination
