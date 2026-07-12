def create_map_link(latitude, longitude):

    return {
        "latitude": latitude,
        "longitude": longitude,
        "map_url": (
            f"https://www.openstreetmap.org/"
            f"?mlat={latitude}&mlon={longitude}"
        )
    }