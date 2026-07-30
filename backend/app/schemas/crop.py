from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import GrowthStage


class CropBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )

    variety: str = Field(
        min_length=2,
        max_length=150,
    )

    planting_date: date

    expected_harvest_date: date

    status: str = Field(
        min_length=2,
        max_length=50,
    )

    growth_stage: GrowthStage

    season: str = Field(
        min_length=2,
        max_length=50,
    )

    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class CropCreate(CropBase):
    field_id: int


class CropUpdate(BaseModel):
    name: str | None = None
    variety: str | None = None
    planting_date: date | None = None
    expected_harvest_date: date | None = None
    status: str | None = None
    growth_stage: GrowthStage | None = None
    season: str | None = None
    notes: str | None = None


class CropRead(CropBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    field_id: int
