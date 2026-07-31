from pydantic import BaseModel, ConfigDict


class CropKnowledgeBase(BaseModel):
    common_name: str
    scientific_name: str
    family: str
    description: str

    optimal_ph_min: float
    optimal_ph_max: float

    min_temperature: float
    max_temperature: float

    water_requirement: str
    growth_duration_days: int

    source: str


class CropKnowledgeCreate(CropKnowledgeBase):
    pass


class CropKnowledgeUpdate(BaseModel):
    common_name: str | None = None
    scientific_name: str | None = None
    family: str | None = None
    description: str | None = None

    optimal_ph_min: float | None = None
    optimal_ph_max: float | None = None

    min_temperature: float | None = None
    max_temperature: float | None = None

    water_requirement: str | None = None
    growth_duration_days: int | None = None

    source: str | None = None


class CropKnowledgeRead(CropKnowledgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
