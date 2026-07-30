from sqlalchemy import desc, select

from app.models.soil_analysis import SoilAnalysis
from app.repositories.base_repository import BaseRepository


class SoilAnalysisRepository(BaseRepository):
    model = SoilAnalysis

    def get_latest(
        self,
        field_id: int,
    ):
        return self.db.scalar(
            select(SoilAnalysis)
            .where(
                SoilAnalysis.field_id == field_id,
            )
            .order_by(
                desc(SoilAnalysis.analysis_date),
            )
            .limit(1)
        )
