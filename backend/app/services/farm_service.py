from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.models.user import User
from app.repositories.farm_repository import FarmRepository
from app.schemas.farm import FarmCreate, FarmUpdate
from app.services.base_owned_service import BaseOwnedService


class FarmService(BaseOwnedService):

    object_name = "Farm"

    def __init__(self, db: Session):
        repository = FarmRepository(db)

        super().__init__(repository)

    def get_farms(self, user: User):
        return self.repository.get_for_user(user)

    def create_farm(
        self,
        data: FarmCreate,
        owner: User,
    ):
        farm = Farm(
            name=data.name,
            location=data.location,
            owner_id=owner.id,
        )

        return self.create(farm)

    def get_farm(
        self,
        farm_id: int,
        user: User,
    ):
        farm = self.get_by_id(farm_id)

        self.check_owner(
            farm.owner_id,
            user,
        )

        return farm

    def update_farm(
        self,
        farm_id: int,
        data: FarmUpdate,
        user: User,
    ):
        farm = self.get_farm(
            farm_id,
            user,
        )

        if data.name is not None:
            farm.name = data.name

        if data.location is not None:
            farm.location = data.location

        return self.update(farm)

    def delete_farm(
        self,
        farm_id: int,
        user: User,
    ):
        farm = self.get_farm(
            farm_id,
            user,
        )

        self.delete(farm)
