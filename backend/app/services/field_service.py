from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.user import User
from app.repositories.farm_repository import FarmRepository
from app.repositories.field_repository import FieldRepository
from app.schemas.field import FieldCreate, FieldUpdate
from app.services.base_owned_service import BaseOwnedService


class FieldService(BaseOwnedService):

    object_name = "Field"

    def __init__(self, db: Session):
        repository = FieldRepository(db)

        super().__init__(repository)

        self.farm_repository = FarmRepository(db)

    def get_fields(self):
        return self.get_all()

    def create_field(
        self,
        data: FieldCreate,
        user: User,
    ):
        farm = self.farm_repository.get_by_id(data.farm_id)

        if farm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found",
            )

        self.check_owner(
            farm.owner_id,
            user,
        )

        field = Field(
            name=data.name,
            area_hectares=data.area_hectares,
            latitude=data.latitude,
            longitude=data.longitude,
            soil_type=data.soil_type,
            farm_id=data.farm_id,
        )

        return self.create(field)

    def get_field(
        self,
        field_id: int,
        user: User,
    ):
        field = self.get_by_id(field_id)

        farm = self.farm_repository.get_by_id(field.farm_id)

        self.check_owner(
            farm.owner_id,
            user,
        )

        return field

    def update_field(
        self,
        field_id: int,
        data: FieldUpdate,
        user: User,
    ):
        field = self.get_field(
            field_id,
            user,
        )

        if data.name is not None:
            field.name = data.name

        if data.area_hectares is not None:
            field.area_hectares = data.area_hectares

        if data.latitude is not None:
            field.latitude = data.latitude

        if data.longitude is not None:
            field.longitude = data.longitude

        if data.soil_type is not None:
            field.soil_type = data.soil_type

        return self.update(field)

    def delete_field(
        self,
        field_id: int,
        user: User,
    ):
        field = self.get_field(
            field_id,
            user,
        )

        self.delete(field)
