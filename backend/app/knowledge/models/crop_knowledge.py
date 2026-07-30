from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CropKnowledge(Base):
    __tablename__ = "crop_knowledge"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    common_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    scientific_name: Mapped[str] = mapped_column(
        String(150),
    )

    family: Mapped[str] = mapped_column(
        String(100),
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    optimal_ph_min: Mapped[float] = mapped_column(
        Float,
    )

    optimal_ph_max: Mapped[float] = mapped_column(
        Float,
    )

    min_temperature: Mapped[float] = mapped_column(
        Float,
    )

    max_temperature: Mapped[float] = mapped_column(
        Float,
    )

    water_requirement: Mapped[str] = mapped_column(
        String(50),
    )

    growth_duration_days: Mapped[int] = mapped_column(
        Integer,
    )

    source: Mapped[str] = mapped_column(
        String(100),
    )
