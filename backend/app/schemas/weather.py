from datetime import date

from pydantic import BaseModel, ConfigDict


class WeatherBase(BaseModel):
    forecast_date: date
    temperature_min: float
    temperature_max: float
    humidity: float
    rainfall: float
    wind_speed: float
    weather_condition: str
    source: str = "Open-Meteo"
    field_id: int


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(BaseModel):
    forecast_date: date | None = None
    temperature_min: float | None = None
    temperature_max: float | None = None
    humidity: float | None = None
    rainfall: float | None = None
    wind_speed: float | None = None
    weather_condition: str | None = None
    source: str | None = None


class WeatherRead(WeatherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
