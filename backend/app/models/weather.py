from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)

    field_id: Mapped[int] = mapped_column(
        ForeignKey("fields.id"),
        nullable=False,
    )

    forecast_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    temperature_min: Mapped[float] = mapped_column(Float)

    temperature_max: Mapped[float] = mapped_column(Float)

    humidity: Mapped[float] = mapped_column(Float)

    rainfall: Mapped[float] = mapped_column(Float)

    wind_speed: Mapped[float] = mapped_column(Float)

    weather_condition: Mapped[str] = mapped_column(String(100))

    source: Mapped[str] = mapped_column(
        String(100),
        default="Open-Meteo",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    field = relationship(
        "Field",
        back_populates="weather_forecasts",
    )
