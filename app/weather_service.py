import requests
from .config import OPENWEATHER_API_KEY


def get_weather(location):

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={location}"
        f"&appid={OPENWEATHER_API_KEY}"
        "&units=metric"
    )


    response = requests.get(url)


    if response.status_code != 200:
        return None


    data = response.json()


    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }