from sqlalchemy import desc, select

from app.models.crop import Crop
from app.repositories.base_repository import BaseRepository


class CropRepository(BaseRepository):
    model = Crop

    def get_active_by_field(
        self,
        field_id: int,
    ) -> Crop | None:
        crop = self.db.scalar(
            select(Crop)
            .where(
                Crop.field_id == field_id,
                Crop.status == "ACTIVE",
            )
            .order_by(
                desc(Crop.planting_date),
            )
            .limit(1)
        )

        if crop is not None:
            return crop

        return self.db.scalar(
            select(Crop)
            .where(
                Crop.field_id == field_id,
            )
            .order_by(
                desc(Crop.planting_date),
            )
            .limit(1)
        )