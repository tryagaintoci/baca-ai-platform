from fastapi import APIRouter

from app.recommendations.engine import RecommendationEngine

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

engine = RecommendationEngine()


@router.get("/")
def get_recommendations():

    return {"message": "Recommendation engine ready"}
