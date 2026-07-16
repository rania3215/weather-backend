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


def get_forecast(location):

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Location not found")

    data = response.json()

    forecast = []

    for item in data["list"]:
        forecast.append({
            "date": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"]
        })

    return forecast[::8][:5]

def get_weather_by_coordinates(latitude, longitude):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }


    response = requests.get(
        url,
        params=params
    )


    if response.status_code != 200:
        raise Exception("Weather not found")


    data = response.json()


    return {

        "location": data["name"],

        "temperature": data["main"]["temp"],

        "humidity": data["main"]["humidity"],

        "description": data["weather"][0]["description"]

    }

