from pydantic import BaseModel
from datetime import date


class WeatherCreate(BaseModel):
    location: str
    start_date: date
    end_date: date


class WeatherResponse(BaseModel):
    id: int
    location: str
    temperature: float
    humidity: float
    description: str

    class Config:
        from_attributes = True