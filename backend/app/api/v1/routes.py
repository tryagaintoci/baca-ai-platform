from fastapi import APIRouter

from fastapi import APIRouter

from app.api.v1.health import router as health_router

router = APIRouter()

router.include_router(health_router)


@router.get("/")
def root():
    return {
        "message": "Welcome to BACA AI Platform"
    }