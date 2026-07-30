from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.integrations.open_meteo import OpenMeteoClient
from app.integrations.weather_codes import WEATHER_CODES
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
    ) -> list[Weather]:
        if current_user.role == UserRole.ADMIN:
            return self.get_all()

        return self.repository.get_for_user(current_user)

    def create_weather(
        self,
        weather_data: WeatherCreate,
        current_user: User,
    ) -> Weather:
        field = self.field_repository.get_by_id(
            weather_data.field_id,
        )

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        self.check_owner(
            field.farm.owner_id,
            current_user,
        )

        weather = Weather(
            **weather_data.model_dump(),
        )

        return self.create(weather)

    def get_weather(
        self,
        weather_id: int,
        current_user: User,
    ) -> Weather:
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
    ) -> Weather:
        weather = self.get_weather(
            weather_id,
            current_user,
        )

        for key, value in weather_data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(weather, key, value)

        return self.update(weather)

    def delete_weather(
        self,
        weather_id: int,
        current_user: User,
    ) -> None:
        weather = self.get_weather(
            weather_id,
            current_user,
        )

        self.delete(weather)

    def sync_weather(
        self,
        field_id: int,
        current_user: User,
    ):
        field = self.field_repository.get_by_id(field_id)

        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Field not found",
            )

        self.check_owner(
            field.farm.owner_id,
            current_user,
        )

        client = OpenMeteoClient()

        data = client.get_forecast(
            field.latitude,
            field.longitude,
        )

        daily = data["daily"]

        forecasts = []

        with self.repository.db.begin():
            for i in range(len(daily["time"])):
                forecast = self.repository.get_by_field_and_date(
                    field.id,
                    date.fromisoformat(daily["time"][i]),
                )

                if forecast is None:
                    forecast = Weather(
                        field_id=field.id,
                        forecast_date=date.fromisoformat(daily["time"][i]),
                    )

                forecast.temperature_min = daily["temperature_2m_min"][i]
                forecast.temperature_max = daily["temperature_2m_max"][i]
                forecast.rainfall = daily["precipitation_sum"][i]
                forecast.wind_speed = daily["windspeed_10m_max"][i]
                forecast.humidity = daily["relative_humidity_2m_mean"][i]

                code = daily["weathercode"][i]

                forecast.weather_condition = WEATHER_CODES.get(
                    code,
                    f"Unknown ({code})",
                )

            forecast.source = "Open-Meteo"

            if forecast.id is None:
                self.repository.db.add(forecast)
                forecasts.append(forecast)
            else:
                forecasts.append(forecast)

            return forecasts
