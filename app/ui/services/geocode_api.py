import httpx

async def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=18"
    headers = {"User-Agent": "FletRideSim/1.0"}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                return data.get("display_name", "Unknown location")
    except Exception as e:
        return f"Error: {e}"
    return "Unknown location"
