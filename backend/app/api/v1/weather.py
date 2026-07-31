from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.weather import (
    WeatherCreate,
    WeatherRead,
    WeatherUpdate,
)
from app.services.weather_service import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.get(
    "/",
    response_model=list[WeatherRead],
)
def get_weather_forecasts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    return service.get_weather_forecasts(current_user)


@router.post(
    "/sync/{field_id}",
    response_model=list[WeatherRead],
)
def sync_weather(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    return service.sync_weather(
        field_id,
        current_user,
    )


@router.get(
    "/{weather_id}",
    response_model=WeatherRead,
)
def get_weather(
    weather_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    return service.get_weather(
        weather_id,
        current_user,
    )


@router.post(
    "/",
    response_model=WeatherRead,
    status_code=status.HTTP_201_CREATED,
)
def create_weather(
    weather_data: WeatherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    return service.create_weather(
        weather_data,
        current_user,
    )


@router.put(
    "/{weather_id}",
    response_model=WeatherRead,
)
def update_weather(
    weather_id: int,
    weather_data: WeatherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    return service.update_weather(
        weather_id,
        weather_data,
        current_user,
    )


@router.delete(
    "/{weather_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_weather(
    weather_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WeatherService(db)

    service.delete_weather(
        weather_id,
        current_user,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
