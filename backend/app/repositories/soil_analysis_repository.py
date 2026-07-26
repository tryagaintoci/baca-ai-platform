from app.models.soil_analysis import SoilAnalysis
from app.repositories.base_repository import BaseRepository


class SoilAnalysisRepository(BaseRepository):

    model = SoilAnalysis
