from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.crop import CropCreate, CropRead, CropUpdate
from app.services.crop_service import CropService

router = APIRouter(
    prefix="/crops",
    tags=["Crops"],
)


@router.get("/", response_model=list[CropRead])
def get_crops(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CropService(db)

    return service.get_crops(current_user)


@router.get("/{crop_id}", response_model=CropRead)
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CropService(db)

    return service.get_crop(
        crop_id,
        current_user,
    )


@router.post("/", response_model=CropRead, status_code=201)
def create_crop(
    crop: CropCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CropService(db)

    return service.create_crop(
        crop,
        current_user,
    )


@router.put("/{crop_id}", response_model=CropRead)
def update_crop(
    crop_id: int,
    crop: CropUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CropService(db)

    return service.update_crop(
        crop_id,
        crop,
        current_user,
    )


@router.delete("/{crop_id}", status_code=204)
def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CropService(db)

    service.delete_crop(
        crop_id,
        current_user,
    )
