from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class WeatherBase(BaseModel):
    forecast_date: date

    temperature_min: float = Field(
        ...,
        description="Minimum temperature (°C)",
    )

    temperature_max: float = Field(
        ...,
        description="Maximum temperature (°C)",
    )

    humidity: float = Field(
        ...,
        ge=0,
        le=100,
        description="Relative humidity (%)",
    )

    rainfall: float = Field(
        ...,
        ge=0,
        description="Rainfall (mm)",
    )

    wind_speed: float = Field(
        ...,
        ge=0,
        description="Wind speed (km/h)",
    )

    weather_condition: str = Field(
        ...,
        max_length=100,
    )

    source: str = Field(
        default="Open-Meteo",
        max_length=100,
    )

    field_id: int


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(BaseModel):
    forecast_date: date | None = None
    temperature_min: float | None = None
    temperature_max: float | None = None
    humidity: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )
    rainfall: float | None = Field(
        default=None,
        ge=0,
    )
    wind_speed: float | None = Field(
        default=None,
        ge=0,
    )
    weather_condition: str | None = Field(
        default=None,
        max_length=100,
    )
    source: str | None = Field(
        default=None,
        max_length=100,
    )


class WeatherRead(WeatherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
