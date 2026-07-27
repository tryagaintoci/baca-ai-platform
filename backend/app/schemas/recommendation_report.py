from datetime import datetime

from pydantic import BaseModel

from app.schemas.recommendation import Recommendation


class RecommendationReport(BaseModel):

    generated_at: datetime

    crop: str

    recommendations: list[Recommendation]
