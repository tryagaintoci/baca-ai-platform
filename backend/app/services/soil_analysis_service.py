from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.models.soil_analysis import SoilAnalysis
from app.models.user import User
from app.repositories.field_repository import FieldRepository
from app.repositories.soil_analysis_repository import SoilAnalysisRepository
from app.schemas.soil_analysis import (
    SoilAnalysisCreate,
    SoilAnalysisUpdate,
)
from app.services.base_owned_service import BaseOwnedService


class SoilAnalysisService(BaseOwnedService):

    object_name = "Soil analysis"

    def __init__(self, db: Session):
        repository = SoilAnalysisRepository(db)

        super().__init__(repository)

        self.field_repository = FieldRepository(db)

    def get_analyses(
        self,
        current_user: User,
    ):
        if current_user.role == UserRole.ADMIN:
            return self.get_all()

        analyses = []

        fields = self.field_repository.get_by_owner(current_user.id)

        for field in fields:
            analyses.extend(field.soil_analyses)

        return analyses

    def create_analysis(
        self,
        analysis_data: SoilAnalysisCreate,
        current_user: User,
    ):
        field = self.field_repository.get_by_id(analysis_data.field_id)

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        self.check_owner(
            field.farm.owner_id,
            current_user,
        )

        analysis = SoilAnalysis(**analysis_data.model_dump())

        return self.create(analysis)

    def get_analysis(
        self,
        analysis_id: int,
        current_user: User,
    ):
        analysis = self.get_by_id(analysis_id)

        self.check_owner(
            analysis.field.farm.owner_id,
            current_user,
        )

        return analysis

    def update_analysis(
        self,
        analysis_id: int,
        analysis_data: SoilAnalysisUpdate,
        current_user: User,
    ):
        analysis = self.get_analysis(
            analysis_id,
            current_user,
        )

        for key, value in analysis_data.model_dump(exclude_unset=True).items():
            setattr(analysis, key, value)

        return self.update(analysis)

    def delete_analysis(
        self,
        analysis_id: int,
        current_user: User,
    ):
        analysis = self.get_analysis(
            analysis_id,
            current_user,
        )

        self.delete(analysis)
