
from datetime import datetime

from .database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date

class WeatherRecord(Base):
  
    __tablename__ = "weather_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    location = Column(
        String,
        nullable=False
    )

    temperature = Column(
        Float
    )

    humidity = Column(
        Float
    )

    description = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    start_date = Column(Date)
    end_date = Column(Date)