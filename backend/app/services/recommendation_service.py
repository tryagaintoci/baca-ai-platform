from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.core.enums import UserRole
from app.models.user import User
from app.recommendations.engine import RecommendationEngine
from app.recommendations.scoring import (
    calculate_health_score,
    calculate_risk_level,
)
from app.repositories.crop_repository import CropRepository
from app.repositories.field_repository import FieldRepository
from app.repositories.soil_analysis_repository import SoilAnalysisRepository
from app.repositories.weather_repository import WeatherRepository
from app.schemas.recommendation_report import RecommendationReport


class RecommendationService:
    def __init__(self, db):
        self.field_repository = FieldRepository(db)
        self.weather_repository = WeatherRepository(db)
        self.soil_repository = SoilAnalysisRepository(db)
        self.crop_repository = CropRepository(db)
        self.engine = RecommendationEngine()

    def generate(
        self,
        field_id: int,
        current_user: User,
    ) -> RecommendationReport:
        field = self.field_repository.get_by_id(field_id)

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        if (
            current_user.role != UserRole.ADMIN
            and field.farm.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        weather = self.weather_repository.get_latest(field_id)

        if weather is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Weather data not found",
            )

        soil = self.soil_repository.get_latest(field_id)

        if soil is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Soil analysis not found",
            )

        crop = self.crop_repository.get_active_by_field(field_id)

        if crop is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found",
            )

        recommendations = self.engine.generate(
            weather,
            soil,
            crop,
        )

        health_score = calculate_health_score(
            weather,
            soil,
            crop,
        )

        risk_level = calculate_risk_level(
            health_score,
        )

        return RecommendationReport(
            generated_at=datetime.now(UTC),
            field_id=field_id,
            crop=crop.name,
            health_score=health_score,
            risk_level=risk_level,
            recommendations=recommendations,
        )