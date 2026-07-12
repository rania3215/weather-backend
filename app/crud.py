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


# UPDATE
def update_weather(
        db: Session,
        record_id: int,
        location: str
):

    record = get_weather_by_id(db, record_id)

    if record:
        record.location = location
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