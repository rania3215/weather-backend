from pydantic import BaseModel


class WeatherCreate(BaseModel):
    location: str



class WeatherResponse(BaseModel):
    id: int
    location: str
    temperature: float
    humidity: float
    description: str

    class Config:
        from_attributes = True