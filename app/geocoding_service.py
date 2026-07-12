import requests
from .config import OPENWEATHER_API_KEY

API_KEY = OPENWEATHER_API_KEY


def get_location_coordinates(location):

    url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={location}"
        f"&limit=1"
        f"&appid={API_KEY}"
    )


    response = requests.get(url)


    if response.status_code != 200:
        return None


    data = response.json()


    if len(data) == 0:
        return None


    return {
        "name": data[0]["name"],
        "country": data[0].get("country"),
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"]
    }