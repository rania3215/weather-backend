import requests
from .config import OPENWEATHER_API_KEY

API_KEY = OPENWEATHER_API_KEY


def get_air_quality(latitude, longitude):

    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={latitude}"
        f"&lon={longitude}"
        f"&appid={API_KEY}"
    )


    response = requests.get(url)


    if response.status_code != 200:
        return None


    data = response.json()


    air_data = data["list"][0]


    return {
        "aqi": air_data["main"]["aqi"],
        "co": air_data["components"]["co"],
        "no2": air_data["components"]["no2"],
        "pm2_5": air_data["components"]["pm2_5"],
        "o3": air_data["components"]["o3"]
    }