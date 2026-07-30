from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import GrowthStage
from app.database.base import Base


class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))

    variety: Mapped[str] = mapped_column(String(150))

    planting_date: Mapped[date] = mapped_column(Date)

    expected_harvest_date: Mapped[date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(String(50))

    growth_stage: Mapped[GrowthStage] = mapped_column(
        Enum(GrowthStage),
        default=GrowthStage.VEGETATIVE,
    )

    season: Mapped[str] = mapped_column(String(50))

    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))

    field = relationship(
        "Field",
        back_populates="crops",
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
