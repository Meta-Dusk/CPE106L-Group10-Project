import random
import asyncio
import math

from geopy.distance import geodesic
from app.ui.map_view import state, render


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


async def simulate_booking(
    pickup, destination, status_callback,
    page, image_grid,
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
    render.render_map(page, image_grid, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status)

    # === Step 2: Simulate driver approaching pickup ===
    steps_to_pickup = 5
    for i in range(1, steps_to_pickup + 1):
        await asyncio.sleep(1)
        pct = i / steps_to_pickup
        lat = driver_location[0] + (pickup[0] - driver_location[0]) * pct
        lon = driver_location[1] + (pickup[1] - driver_location[1]) * pct

        state.driver_marker[0] = (lat, lon)
        render.render_map(page, image_grid, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status)

        dist = geodesic((lat, lon), pickup).km
        status_callback(f"Driver approaching... {dist * 1000:.0f}m away")

    # === Step 3: Picked up ===
    status_callback("Driver has arrived. Picking you up...")
    await asyncio.sleep(2)

    # === Step 4: En route to destination ===
    steps_to_destination = 6
    for i in range(1, steps_to_destination + 1):
        await asyncio.sleep(1)
        pct = i / steps_to_destination
        lat = pickup[0] + (destination[0] - pickup[0]) * pct
        lon = pickup[1] + (destination[1] - pickup[1]) * pct

        state.driver_marker[0] = (lat, lon)
        render.render_map(page, image_grid, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status)

        dist_remaining = geodesic((lat, lon), destination).km
        status_callback(f"En route... {dist_remaining:.2f} km remaining")

    # === Step 5: Arrived ===
    state.driver_marker[0] = destination
    render.render_map(page, image_grid, pickup_lat_input, pickup_lon_input, dest_lat_input, dest_lon_input, pin_status)

    status_callback("Arrived at destination. Thank you for riding! 🚗")
    return destination
