import requests
from .config import YOUTUBE_API_KEY


def get_youtube_videos(location):

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "key": YOUTUBE_API_KEY,
        "q": f"{location} travel",
        "part": "snippet",
        "maxResults": 5,
        "type": "video"
    }


    response = requests.get(
        url,
        params=params
    )


    if response.status_code != 200:
        return None


    data = response.json()


    videos = []


    for item in data["items"]:

        videos.append({

            "title": item["snippet"]["title"],

            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],

            "url": 
            f"https://www.youtube.com/watch?v={item['id']['videoId']}"

        })


    return {
        "location": location,
        "videos": videos
    }