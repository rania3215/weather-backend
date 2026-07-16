from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, SessionLocal, Base
from . import models
from . import crud
from dicttoxml import dicttoxml

from .schemas import WeatherCreate
from .weather_service import get_weather
from fastapi.responses import FileResponse , Response
from .export_service import export_to_csv

from .geocoding_service import get_location_coordinates
from .air_quality_service import get_air_quality
from app.weather_service import get_forecast
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.weather_service import get_weather_by_coordinates
from .youtube_service import get_youtube_videos

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Weather Backend API",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@app.get("/")
def home():

    return {
        "message": "Weather API running"
    }



# CREATE
@app.post("/weather")
def create_weather(
    weather: WeatherCreate,
    db: Session = Depends(get_db)
):

    # Get weather from API
    result = get_weather(weather.location)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=" Enter location"
        )


    # Save record
    new_record = models.WeatherRecord(

        location=weather.location,

        temperature=result["temperature"],

        humidity=result["humidity"],

        description=result["description"]

    )


    db.add(new_record)

    db.commit()

    db.refresh(new_record)


    return new_record



# READ ALL
@app.get("/weather")
def read_weather(
    db: Session = Depends(get_db)
):

    records = crud.get_weather_records(db)

    return records


@app.get("/export/xml")
def exportXML(
db:Session=Depends(get_db)
):

    records=crud.get_weather_records(db)

    xml=dicttoxml(
        [
        {
        "location":r.location,
        "temperature":r.temperature,
        "humidity":r.humidity
        }
        for r in records
        ]
    )

    return Response(
        content=xml,
        media_type="application/xml",
        headers={
        "Content-Disposition": "attachment; filename=weather_export.xml"
    }
    )

# READ ONE
@app.get("/weather/{record_id}")
def read_weather_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):

    record = crud.get_weather_by_id(
        db,
        record_id
    )


    if record is None:

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )


    return record



# UPDATE
@app.put("/weather/{record_id}")
def update_weather(
    record_id: int,
    location: str,
    db: Session = Depends(get_db)
):

    location = location.strip()

    updated = crud.update_weather(
        db,
        record_id,
        location
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return updated



# DELETE
@app.delete("/weather/{record_id}")
def delete_weather(
    record_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_weather(
        db,
        record_id
    )


    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )


    return {
        "message": "Record deleted successfully"
    }

@app.get("/export/csv")
def export_csv(
    db: Session = Depends(get_db)
):

    records = crud.get_weather_records(db)


    file = export_to_csv(records)


    return FileResponse(
        path=file,
        filename="weather_export.csv",
        media_type="text/csv"
    )

@app.get("/location/{location}")
def get_location(location: str):

    result = get_location_coordinates(location)


    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )


    return result

@app.get("/forecast/{location}")
def forecast_weather(location: str):

    try:

        return {
            "location": location,
            "forecast": get_forecast(location)
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@app.get("/export/json")
def export_weather_json(
    db: Session = Depends(get_db)
):

    records = crud.get_weather_records(db)

    return JSONResponse(
        content=[
            {
                "id": record.id,
                "location": record.location,
                "temperature": record.temperature,
                "humidity": record.humidity,
                "description": record.description,
                "created_at": str(record.created_at)
            }
            for record in records
        ]
    )
@app.get("/weather/location/{latitude}/{longitude}")
def weather_by_coordinates(latitude: float, longitude: float):

    try:
        return get_weather_by_coordinates(
            latitude,
            longitude
        )

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@app.get("/map-coordinates/{latitude}/{longitude}")
def get_map_coordinates(latitude: float, longitude: float):

    return {
        "latitude": latitude,
        "longitude": longitude,
        "map_url": 
        f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}"
    }

@app.get("/air-quality-coordinates/{latitude}/{longitude}")
def air_quality_coordinates(latitude: float, longitude: float):

    result = get_air_quality(
        latitude,
        longitude
    )

    if result is None:
        raise HTTPException(
            status_code=500,
            detail="Air quality service unavailable"
        )

    return {
        "air_quality": result
    }


@app.get("/youtube/{location}")
def youtube_videos(location: str):

    try:
        return get_youtube_videos(location)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/map-coordinates/{latitude}/{longitude}")
def map_by_coordinates(latitude: float, longitude: float):

    return {
        "latitude": latitude,
        "longitude": longitude,
        "map_url": f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}"
    }
@app.get("/air-quality-coordinates/{latitude}/{longitude}")
def air_quality_by_coordinates(latitude: float, longitude: float):

    result = get_air_quality(latitude, longitude)

    if result is None:
        raise HTTPException(status_code=500, detail="Air quality unavailable")

    return {
        "location": "Current Location",
        "country": "",
        "air_quality": result
    }