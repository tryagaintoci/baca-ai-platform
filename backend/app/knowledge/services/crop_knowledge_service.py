from fastapi import HTTPException, status

from app.knowledge.models import CropKnowledge
from app.knowledge.repositories.crop_knowledge_repository import (
    CropKnowledgeRepository,
)


class CropKnowledgeService:
    def __init__(self, db):
        self.repository = CropKnowledgeRepository(db)

    def get_all(self):
        return self.repository.get_all()

    def get_by_name(
        self,
        name: str,
    ):
        crop = self.repository.get_by_name(name)

        if crop is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found",
            )

        return crop

    def create(
        self,
        data,
    ):
        crop = CropKnowledge(**data.model_dump())

        return self.repository.create(crop)
