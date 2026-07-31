from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.soil_analysis import (
    SoilAnalysisCreate,
    SoilAnalysisRead,
    SoilAnalysisUpdate,
)
from app.services.soil_analysis_service import SoilAnalysisService

router = APIRouter(
    prefix="/soil-analyses",
    tags=["Soil Analyses"],
)


@router.get("/", response_model=list[SoilAnalysisRead])
def get_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SoilAnalysisService(db)
    return service.get_analyses(current_user)


@router.get("/{analysis_id}", response_model=SoilAnalysisRead)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SoilAnalysisService(db)
    return service.get_analysis(
        analysis_id,
        current_user,
    )


@router.post("/", response_model=SoilAnalysisRead, status_code=201)
def create_analysis(
    analysis: SoilAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SoilAnalysisService(db)
    return service.create_analysis(
        analysis,
        current_user,
    )


@router.put("/{analysis_id}", response_model=SoilAnalysisRead)
def update_analysis(
    analysis_id: int,
    analysis: SoilAnalysisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SoilAnalysisService(db)
    return service.update_analysis(
        analysis_id,
        analysis,
        current_user,
    )


@router.delete("/{analysis_id}", status_code=204)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SoilAnalysisService(db)

    service.delete_analysis(
        analysis_id,
        current_user,
    )
