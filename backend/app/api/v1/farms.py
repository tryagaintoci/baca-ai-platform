from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.farm import FarmCreate, FarmRead, FarmUpdate
from app.services.farm_service import FarmService

router = APIRouter(
    prefix="/farms",
    tags=["Farms"],
)


@router.get("/", response_model=list[FarmRead])
def get_farms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmService(db)
    return service.get_farms(current_user)


@router.post("/", response_model=FarmRead, status_code=201)
def create_farm(
    farm: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmService(db)

    return service.create_farm(
        farm,
        current_user,
    )


@router.get("/{farm_id}", response_model=FarmRead)
def get_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmService(db)
    return service.get_farm(farm_id, current_user)


@router.put("/{farm_id}", response_model=FarmRead)
def update_farm(
    farm_id: int,
    farm: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmService(db)
    return service.update_farm(
        farm_id,
        farm,
        current_user,
    )


@router.delete("/{farm_id}", status_code=204)
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmService(db)

    service.delete_farm(
        farm_id,
        current_user,
    )
