from sqlalchemy import select

from app.models.farm import Farm
from app.models.field import Field
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class FieldRepository(BaseRepository):
    model = Field

    def get_for_user(self, user: User):
        return self.get_by_owner(user.id)

    def get_by_owner(self, owner_id: int):
        return list(
            self.db.scalars(
                select(Field).join(Farm).where(Farm.owner_id == owner_id)
            ).all()
        )
