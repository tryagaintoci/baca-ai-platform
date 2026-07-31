from sqlalchemy import select
from sqlalchemy.orm import Session

from app.knowledge.models import CropKnowledge


class CropKnowledgeRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_all(self):
        return self.db.scalars(select(CropKnowledge)).all()

    def get_by_name(
        self,
        name: str,
    ):
        return self.db.scalar(
            select(CropKnowledge).where(CropKnowledge.common_name == name)
        )

    def create(
        self,
        crop: CropKnowledge,
    ):
        self.db.add(crop)
        self.db.commit()
        self.db.refresh(crop)

        return crop
