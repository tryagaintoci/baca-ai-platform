from datetime import date

from pydantic import BaseModel, ConfigDict


class SoilAnalysisBase(BaseModel):
    analysis_date: date
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float
    moisture: float
    laboratory: str
    recommendations: str | None = None


class SoilAnalysisCreate(SoilAnalysisBase):
    field_id: int


class SoilAnalysisUpdate(BaseModel):
    analysis_date: date | None = None
    ph: float | None = None
    nitrogen: float | None = None
    phosphorus: float | None = None
    potassium: float | None = None
    organic_matter: float | None = None
    moisture: float | None = None
    laboratory: str | None = None
    recommendations: str | None = None


class SoilAnalysisRead(SoilAnalysisBase):
    id: int
    field_id: int

    model_config = ConfigDict(from_attributes=True)
