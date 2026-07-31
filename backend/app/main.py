from fastapi import FastAPI

from app.api.v1.router import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="AI platform for agricultural analysis and advisory",
)

app.include_router(router, prefix="/api/v1")
