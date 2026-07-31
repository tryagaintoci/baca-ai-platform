from pydantic import BaseModel, ConfigDict, Field


class FieldBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )

    area_hectares: float = Field(gt=0)

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    soil_type: str = Field(
        min_length=2,
        max_length=100,
    )


class FieldCreate(FieldBase):
    farm_id: int


class FieldUpdate(BaseModel):
    name: str | None = None
    area_hectares: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    soil_type: str | None = None


class FieldRead(FieldBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)
