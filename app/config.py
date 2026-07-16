import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

YOUTUBE_API_KEY = os.getenv(
    "YOUTUBE_API_KEY"
)