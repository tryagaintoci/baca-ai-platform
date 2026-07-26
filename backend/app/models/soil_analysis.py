from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class SoilAnalysis(Base):
    __tablename__ = "soil_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_date: Mapped[date] = mapped_column(Date)

    ph: Mapped[float] = mapped_column(Float)

    nitrogen: Mapped[float] = mapped_column(Float)

    phosphorus: Mapped[float] = mapped_column(Float)

    potassium: Mapped[float] = mapped_column(Float)

    organic_matter: Mapped[float] = mapped_column(Float)

    moisture: Mapped[float] = mapped_column(Float)

    laboratory: Mapped[str] = mapped_column(String(150))

    recommendations: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))

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
        back_populates="soil_analyses",
    )
