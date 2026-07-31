from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.knowledge.schemas.crop_knowledge import (
    CropKnowledgeCreate,
    CropKnowledgeRead,
)
from app.knowledge.services.crop_knowledge_service import (
    CropKnowledgeService,
)

router = APIRouter(
    prefix="/knowledge/crops",
    tags=["Knowledge"],
)


@router.get(
    "/",
    response_model=list[CropKnowledgeRead],
)
def get_crops(
    db: Session = Depends(get_db),
):
    service = CropKnowledgeService(db)

    return service.get_all()


@router.get(
    "/{name}",
    response_model=CropKnowledgeRead,
)
def get_crop(
    name: str,
    db: Session = Depends(get_db),
):
    service = CropKnowledgeService(db)

    return service.get_by_name(name)


@router.post(
    "/",
    response_model=CropKnowledgeRead,
    status_code=201,
)
def create_crop(
    crop: CropKnowledgeCreate,
    db: Session = Depends(get_db),
):
    service = CropKnowledgeService(db)

    return service.create(crop)
