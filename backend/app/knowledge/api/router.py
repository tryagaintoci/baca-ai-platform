from fastapi import APIRouter

from app.knowledge.api.crop_knowledge import router as crop_knowledge_router

router = APIRouter()

router.include_router(crop_knowledge_router)
