from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.models.user import User
from app.models.weather import Weather
from app.repositories.field_repository import FieldRepository
from app.repositories.weather_repository import WeatherRepository
from app.schemas.weather import WeatherCreate, WeatherUpdate
from app.services.base_owned_service import BaseOwnedService


class WeatherService(BaseOwnedService):

    object_name = "Weather forecast"

    def __init__(self, db: Session):
        repository = WeatherRepository(db)

        super().__init__(repository)

        self.field_repository = FieldRepository(db)

    def get_weather_forecasts(
        self,
        current_user: User,
    ):
        if current_user.role == UserRole.ADMIN:
            return self.get_all()

        return self.repository.get_for_user(current_user)

    def create_weather(
        self,
        weather_data: WeatherCreate,
        current_user: User,
    ):
        field = self.field_repository.get_by_id(weather_data.field_id)

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        self.check_owner(
            field.farm.owner_id,
            current_user,
        )

        weather = Weather(**weather_data.model_dump())

        return self.create(weather)

    def get_weather(
        self,
        weather_id: int,
        current_user: User,
    ):
        weather = self.get_by_id(weather_id)

        self.check_owner(
            weather.field.farm.owner_id,
            current_user,
        )

        return weather

    def update_weather(
        self,
        weather_id: int,
        weather_data: WeatherUpdate,
        current_user: User,
    ):
        weather = self.get_weather(
            weather_id,
            current_user,
        )

        for key, value in weather_data.model_dump(exclude_unset=True).items():
            setattr(weather, key, value)

        return self.update(weather)

    def delete_weather(
        self,
        weather_id: int,
        current_user: User,
    ):
        weather = self.get_weather(
            weather_id,
            current_user,
        )

        self.delete(weather)
