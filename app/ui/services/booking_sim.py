import random
import asyncio
import math
import aiohttp
import os

import flet as ft

from geopy.distance import geodesic
from app.ui.map_view import state, render
from app.ui.map_view.ui_elements import get_driver_icon
from app.assets.audio_manager import audio, SFX
from dotenv import load_dotenv
from pathlib import Path


ENV_DIR = Path(__file__).parent.parent / ".env"

if ENV_DIR.exists():
    load_dotenv(dotenv_path=ENV_DIR)
    print("ORS API Key loaded.")
else:
    print("ORS API Key not found...")
    
ORS_API_KEY = os.getenv("ORS_API_KEY")


async def fetch_route_osm(pickup, destination, api_key: str):
    """Fetch a road-based route from OpenRouteService. Returns list of (lat, lon)."""
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    payload = {
        "coordinates": [[pickup[1], pickup[0]], [destination[1], destination[0]]],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status != 200:
                print(f"[ROUTING ERROR] {response.status}: {await response.text()}")
                return None
            data = await response.json()
            coords = data["features"][0]["geometry"]["coordinates"]
            return [(lat, lon) for lon, lat in coords]

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

def format_distance_km(km: float) -> str:
    """Format distance: 500m for <1km, else X.XX km"""
    if km < 1:
        return f"{km * 1000:.0f}m"
    else:
        return f"{km:.2f} km"

def ease_in_out(t):
    """Cubic ease-in-out: accelerates and decelerates smoothly"""
    return 3 * t**2 - 2 * t**3

def interpolate_path(start, end, segments=5, jitter=0.0003):
    path = []
    for i in range(1, segments + 1):
        pct = i / segments
        lat = start[0] + (end[0] - start[0]) * pct
        lon = start[1] + (end[1] - start[1]) * pct
        lat += random.uniform(-jitter, jitter)
        lon += random.uniform(-jitter, jitter)
        path.append((lat, lon))
    return path

async def animate_driver_to(target, duration, page_fps, callback=None, verbose=False):
    steps = int(duration * page_fps)
    start = state.driver_marker[0]
    
    for i in range(steps):
        if state.cancel_simulation_flag[0]:
            print("[CANCEL] Simulation interrupted.")
            return

        t = (i + 1) / steps
        pct = ease_in_out(t)

        lat = start[0] + (target[0] - start[0]) * pct
        lon = start[1] + (target[1] - start[1]) * pct
        state.driver_marker[0] = (lat, lon)
        update_driver_position(lat, lon)
        
        if verbose and callback:
            dist = geodesic((lat, lon), target).km
            callback(f"Driver moving... {dist*1000:.0f}m away")

        await asyncio.sleep((1 / page_fps) * random.uniform(0.9, 1.2))

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
    2. Driver approaching (waypoints)
    3. Pickup
    4. En route to destination (waypoints)
    5. Arrival
    """
    
    state.cancel_simulation_flag[0] = False  # reset before starting
    status_callback("Booking in progress...")

    # === Step 1: Wait for driver match ===
    if state.cancel_simulation_flag[0]:
        print("[CANCEL] Simulation interrupted.")
        return
    
    wait_time = get_random_wait_time()
    status_callback(f"Searching for driver... ETA: {wait_time:.1f}s")
    await asyncio.sleep(wait_time)

    # Generate driver location
    driver_location = get_random_driver_location(*pickup)
    driver_distance = geodesic(pickup, driver_location).km
    status_callback(f"Driver found! {driver_distance:.2f} km away")
    audio.play_sfx(SFX.ALERT)

    state.driver_marker[0] = driver_location
    tile_stack.controls = [c for c in tile_stack.controls if c is not None]
    page.update()

    render.render_map(
        page, tile_stack,
        pickup_lat_input, pickup_lon_input,
        dest_lat_input, dest_lon_input,
        pin_status
    )

    # Ensure driver icon is initialized
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
        tile_stack.controls.append(container)
        safe_update_page(page)

    update_driver_position(*driver_location)
    
    route_path = await fetch_route_osm(pickup, destination, api_key=ORS_API_KEY)
    state.current_debug_path = route_path
    
    if state.show_debug_overlay[0] and route_path:
        render.render_route_debug_overlay(page, tile_stack, route_path)

    # Driver pause realism
    if state.cancel_simulation_flag[0]:
        print("[CANCEL] Simulation interrupted.")
        return
    
    await asyncio.sleep(random.uniform(1.5, 3.5))
    status_callback("Driver is on the way...")

    # === Step 2: Approach pickup via waypoints ===
    if state.cancel_simulation_flag[0]:
        print("[CANCEL] Simulation interrupted.")
        return
    
    pickup_path = interpolate_path(driver_location, pickup, segments=4)
    for wp in pickup_path:
        dist = geodesic(wp, pickup).km
        status_callback(f"Driver approaching... {format_distance_km(dist)} away")
        await animate_driver_to(wp, duration=get_random_wait_time(), page_fps=60, verbose=False)

    # === Step 3: Pickup ===
    if state.cancel_simulation_flag[0]:
        print("[CANCEL] Simulation interrupted.")
        return
    
    audio.play_sfx(SFX.ALERT)
    status_callback("Driver has arrived. Picking you up...")
    await asyncio.sleep(2)

    # === Step 4: En route to destination via ORS or fallback ===
    if state.cancel_simulation_flag[0]:
        print("[CANCEL] Simulation interrupted.")
        return

    if route_path and len(route_path) > 1:
        print("[INFO] Using real road path from ORS...")
        render.render_route_debug_overlay(page, tile_stack, route_path)
        for wp in route_path:
            dist = geodesic(wp, destination).km
            status_callback(f"En route... {format_distance_km(dist)} remaining")
            await animate_driver_to(wp, duration=get_random_wait_time(), page_fps=60, verbose=False)
    else:
        print("[WARN] Falling back to linear interpolation.")
        trip_path = interpolate_path(pickup, destination, segments=6)
        for wp in trip_path:
            dist = geodesic(wp, destination).km
            status_callback(f"En route... {format_distance_km(dist)} remaining")
            await animate_driver_to(wp, duration=get_random_wait_time(), page_fps=60, verbose=False)

    # === Step 5: Arrival ===
    state.driver_marker[0] = destination
    update_driver_position(*destination)

    audio.play_sfx(SFX.REWARD)
    status_callback("Arrived at destination. Thank you for riding! 🚗")
    await asyncio.sleep(2)
    status_callback("")
    return destination
