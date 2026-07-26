from fastapi import APIRouter

from app.api.v1 import crops, soil_analyses
from app.api.v1.auth import router as auth_router
from app.api.v1.farms import router as farms_router
from app.api.v1.fields import router as fields_router
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.api.v1.weather import router as weather_router

router = APIRouter()

router.include_router(health_router)
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(farms_router)
router.include_router(fields_router)
router.include_router(crops.router)
router.include_router(soil_analyses.router)
router.include_router(weather_router)


@router.get("/")
def root():
    return {"message": "Welcome to BACA AI Platform"}
