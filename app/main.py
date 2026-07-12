from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, SessionLocal, Base
from . import models
from . import crud

from .schemas import WeatherCreate
from .weather_service import get_weather

from fastapi.responses import FileResponse
from .export_service import export_to_csv

from .geocoding_service import get_location_coordinates

from .map_service import create_map_link

from .air_quality_service import get_air_quality

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Weather Backend API",
    version="1.0"
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

    # Validate dates
    if weather.start_date > weather.end_date:

        raise HTTPException(
            status_code=400,
            detail="Start date must be before end date"
        )


    # Get weather from API
    result = get_weather(weather.location)


    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Location not found"
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

@app.get("/map/{location}")
def get_map(location: str):

    coordinates = get_location_coordinates(location)


    if coordinates is None:

        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )


    map_data = create_map_link(
        coordinates["latitude"],
        coordinates["longitude"]
    )


    return {
        "location": coordinates["name"],
        "country": coordinates["country"],
        **map_data
    }

@app.get("/air-quality/{location}")
def air_quality(location: str):

    coordinates = get_location_coordinates(location)


    if coordinates is None:

        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )


    result = get_air_quality(
        coordinates["latitude"],
        coordinates["longitude"]
    )


    if result is None:

        raise HTTPException(
            status_code=500,
            detail="Air quality service unavailable"
        )


    return {
        "location": coordinates["name"],
        "country": coordinates["country"],
        "air_quality": result
    }