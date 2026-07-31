from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.crop import Crop
    from app.models.farm import Farm
    from app.models.soil_analysis import SoilAnalysis
    from app.models.weather import Weather


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    area_hectares: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    soil_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"),
        nullable=False,
        index=True,
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

    farm: Mapped["Farm"] = relationship(
        back_populates="fields",
    )

    crops: Mapped[list["Crop"]] = relationship(
        back_populates="field",
        cascade="all, delete-orphan",
    )

    soil_analyses: Mapped[list["SoilAnalysis"]] = relationship(
        back_populates="field",
        cascade="all, delete-orphan",
    )

    weather_forecasts: Mapped[list["Weather"]] = relationship(
        back_populates="field",
        cascade="all, delete-orphan",
    )
