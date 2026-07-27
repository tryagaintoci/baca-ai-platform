from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.field import Field


class Weather(Base):
    __tablename__ = "weather"

    __table_args__ = (
        UniqueConstraint(
            "field_id",
            "forecast_date",
            name="uq_weather_field_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    field_id: Mapped[int] = mapped_column(
        ForeignKey("fields.id"),
        nullable=False,
        index=True,
    )

    forecast_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    temperature_min: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    temperature_max: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    humidity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rainfall: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    wind_speed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    weather_condition: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Open-Meteo",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    field: Mapped["Field"] = relationship(
        back_populates="weather_forecasts",
    )
