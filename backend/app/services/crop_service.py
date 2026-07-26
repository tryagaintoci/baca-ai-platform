from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.user import User
from app.repositories.crop_repository import CropRepository
from app.repositories.field_repository import FieldRepository
from app.schemas.crop import CropCreate, CropUpdate
from app.services.base_owned_service import BaseOwnedService


class CropService(BaseOwnedService):

    object_name = "Crop"

    def __init__(self, db: Session):
        repository = CropRepository(db)

        super().__init__(repository)

        self.field_repository = FieldRepository(db)

    def get_crops(
        self,
        current_user: User,
    ):
        if current_user.role.name == "ADMIN":
            return self.get_all()

        crops = []

        fields = self.field_repository.get_by_owner(current_user.id)

        for field in fields:
            crops.extend(field.crops)

        return crops

    def create_crop(
        self,
        crop_data: CropCreate,
        current_user: User,
    ):
        field = self.field_repository.get_by_id(crop_data.field_id)

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        self.check_owner(
            field.farm.owner_id,
            current_user,
        )

        crop = Crop(**crop_data.model_dump())

        return self.create(crop)

    def get_crop(
        self,
        crop_id: int,
        current_user: User,
    ):
        crop = self.get_by_id(crop_id)

        self.check_owner(
            crop.field.farm.owner_id,
            current_user,
        )

        return crop

    def update_crop(
        self,
        crop_id: int,
        crop_data: CropUpdate,
        current_user: User,
    ):
        crop = self.get_crop(
            crop_id,
            current_user,
        )

        for key, value in crop_data.model_dump(exclude_unset=True).items():
            setattr(crop, key, value)

        return self.update(crop)

    def delete_crop(
        self,
        crop_id: int,
        current_user: User,
    ):
        crop = self.get_crop(
            crop_id,
            current_user,
        )

        self.delete(crop)
