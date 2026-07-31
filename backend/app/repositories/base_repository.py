from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseRepository:
    model = None

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return list(self.db.scalars(select(self.model)).all())

    def get_by_id(
        self,
        object_id: int,
    ):
        return self.db.get(
            self.model,
            object_id,
        )

    def create(
        self,
        obj,
    ):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(
        self,
        obj,
    ):
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(
        self,
        obj,
    ):
        self.db.delete(obj)
        self.db.commit()
