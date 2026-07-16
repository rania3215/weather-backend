from sqlalchemy.orm import Session
from . import models


# READ - Get all records
def get_weather_records(db: Session):
    return db.query(models.WeatherRecord).all()


# READ - Get one record by ID
def get_weather_by_id(db: Session, record_id: int):
    return (
        db.query(models.WeatherRecord)
        .filter(models.WeatherRecord.id == record_id)
        .first()
    )


def update_weather(db, record_id, location):

    record = db.query(models.WeatherRecord).filter(
        models.WeatherRecord.id == record_id
    ).first()


    if record is None:
        return None


    from .weather_service import get_weather

    weather = get_weather(location)


    if weather is None:
        return None


    record.location = location
    record.temperature = weather["temperature"]
    record.humidity = weather["humidity"]
    record.description = weather["description"]


    db.commit()
    db.refresh(record)


    return record


# DELETE
def delete_weather(
        db: Session,
        record_id: int
):

    record = get_weather_by_id(db, record_id)

    if record:
        db.delete(record)
        db.commit()

    return record