from datetime import datetime

from pydantic import BaseModel

from app.schemas.recommendation import Recommendation


class RecommendationReport(BaseModel):
    generated_at: datetime

    field_id: int

    crop: str

    health_score: int

    risk_level: str

    recommendations: list[Recommendation]
