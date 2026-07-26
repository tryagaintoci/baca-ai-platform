from sqlalchemy import select

from app.models.farm import Farm
from app.repositories.base_repository import BaseRepository


class FarmRepository(BaseRepository):

    model = Farm

    def get_by_owner(self, owner_id: int):
        return list(
            self.db.scalars(select(Farm).where(Farm.owner_id == owner_id)).all()
        )
