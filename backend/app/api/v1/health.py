from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health():
    return {"status": "ok", "service": "BACA AI Platform", "version": "0.3.0"}
