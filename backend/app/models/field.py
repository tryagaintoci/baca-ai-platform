from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))

    area_hectares: Mapped[float] = mapped_column(Float)

    latitude: Mapped[float] = mapped_column(Float)

    longitude: Mapped[float] = mapped_column(Float)

    soil_type: Mapped[str] = mapped_column(String(100))

    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    farm = relationship(
        "Farm",
        back_populates="fields",
    )

    crops = relationship(
        "Crop",
        back_populates="field",
    )

    soil_analyses = relationship(
        "SoilAnalysis",
        back_populates="field",
        cascade="all, delete-orphan",
    )

    weather_forecasts = relationship(
        "Weather",
        back_populates="field",
        cascade="all, delete-orphan",
    )
