import math


TILE_SIZE = 256
TILE_SERVER = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"


def tile_to_latlon(x_tile, y_tile, zoom):
    """Convert tile x/y back to lat/lon (tile center)."""
    n = 2 ** zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

def latlon_to_tile(lat, lon, zoom):
    """Convert lat/lon to tile x/y at a specific zoom level."""
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2 * n)
    return x_tile, y_tile

def latlon_to_tile_and_offset(lat, lon, zoom):
    """Returns the tile X/Y and pixel offset (px, py) within the tile."""
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = (lon + 180.0) / 360.0 * n
    y = (1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2 * n

    tile_x = int(x)
    tile_y = int(y)
    pixel_x = int((x - tile_x) * TILE_SIZE)
    pixel_y = int((y - tile_y) * TILE_SIZE)

    return tile_x, tile_y, pixel_x, pixel_y

def tile_to_url(x, y, z):
    max_tile = 2 ** z - 1
    if x < 0 or x > max_tile or y < 0 or y > max_tile:
        return None  # Invalid tile
    return TILE_SERVER.format(x=x, y=y, z=z)

def build_map_tiles(center_lat, center_lon, zoom):
    cx, cy = latlon_to_tile(center_lat, center_lon, zoom)

    # Generate a 3x3 grid centered on cx, cy
    tiles = []
    for dy in [-1, 0, 1]:
        row = []
        for dx in [-1, 0, 1]:
            tx = cx + dx
            ty = cy + dy
            url = tile_to_url(tx, ty, zoom)
            row.append(url)
        tiles.append(row)
    return tiles

def tile_pixel_to_latlon(x_tile, y_tile, px, py, zoom):
    """Convert tile X/Y + pixel offset to lat/lon."""
    tile_size = 256
    n = 2 ** zoom
    lon_deg = (x_tile * tile_size + px) / (tile_size * n) * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y_tile * tile_size + py) / (tile_size * n))))
    lat_deg = math.degrees(lat_rad)
    return lon_deg, lat_deg