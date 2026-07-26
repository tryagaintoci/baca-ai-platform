from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.field import FieldCreate, FieldRead, FieldUpdate
from app.services.field_service import FieldService

router = APIRouter(
    prefix="/fields",
    tags=["Fields"],
)


@router.get("/", response_model=list[FieldRead])
def get_fields(
    db: Session = Depends(get_db),
):
    service = FieldService(db)
    return service.get_fields()


@router.post("/", response_model=FieldRead, status_code=201)
def create_field(
    field: FieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FieldService(db)

    return service.create_field(
        field,
        current_user,
    )


@router.get("/{field_id}", response_model=FieldRead)
def get_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FieldService(db)
    return service.get_field(field_id, current_user)


@router.put("/{field_id}", response_model=FieldRead)
def update_field(
    field_id: int,
    field: FieldUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FieldService(db)
    return service.update_field(
        field_id,
        field,
        current_user,
    )


@router.delete("/{field_id}", status_code=204)
def delete_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FieldService(db)
    service.delete_field(
        field_id,
        current_user,
    )
