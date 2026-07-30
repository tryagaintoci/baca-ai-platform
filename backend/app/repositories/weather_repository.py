from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.models.farm import Farm
from app.models.field import Field
from app.models.user import User
from app.models.weather import Weather
from app.repositories.base_repository import BaseRepository


class WeatherRepository(BaseRepository):
    model = Weather

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    def get_for_user(
        self,
        user: User,
    ) -> list[Weather]:
        if user.role == UserRole.ADMIN:
            return self.get_all()

        return list(
            self.db.scalars(
                select(Weather).join(Field).join(Farm).where(Farm.owner_id == user.id)
            ).all()
        )

    def get_by_field(
        self,
        field_id: int,
    ) -> list[Weather]:
        return list(
            self.db.scalars(
                select(Weather).where(
                    Weather.field_id == field_id,
                )
            ).all()
        )

    def get_by_field_and_date(
        self,
        field_id: int,
        forecast_date,
    ):
        return self.db.scalar(
            select(Weather)
            .where(
                Weather.field_id == field_id,
                Weather.forecast_date == forecast_date,
            )
            .with_for_update()
        )

    def get_latest(
        self,
        field_id: int,
    ):
        return self.db.scalar(
            select(Weather)
            .where(
                Weather.field_id == field_id,
            )
            .order_by(
                desc(Weather.forecast_date),
            )
            .limit(1)
        )
