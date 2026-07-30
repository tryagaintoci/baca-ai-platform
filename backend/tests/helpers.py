import time
from datetime import date

from fastapi.testclient import TestClient


def get_token(
    client: TestClient,
    email: str = "ahmed@example.com",
    password: str = "Baca123!",
) -> str:
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_farm(
    client: TestClient,
    token: str,
) -> int:
    response = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Farm pytest",
            "location": "Alger",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_field(
    client: TestClient,
    token: str,
    farm_id: int,
) -> dict:
    response = client.post(
        "/api/v1/fields/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Champ pytest",
            "area_hectares": 12.5,
            "latitude": 36.75,
            "longitude": 3.05,
            "soil_type": "Argileux",
            "farm_id": farm_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_crop(
    client: TestClient,
    token: str,
    field_id: int,
) -> dict:
    response = client.post(
        "/api/v1/crops/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Maïs",
            "variety": "Hybrid",
            "planting_date": "2026-09-01",
            "expected_harvest_date": "2027-01-15",
            "status": "Growing",
            "growth_stage": "VEGETATIVE",
            "season": "2026",
            "notes": "Test pytest",
            "field_id": field_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_weather(
    client: TestClient,
    token: str,
    field_id: int,
) -> dict:
    forecast_date = (
        date.fromordinal(date.today().toordinal() + int(time.time() * 1000) % 50000)
    ).isoformat()

    response = client.post(
        "/api/v1/weather/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "forecast_date": forecast_date,
            "temperature_min": 18.5,
            "temperature_max": 31.2,
            "humidity": 68.0,
            "rainfall": 1.5,
            "wind_speed": 12.4,
            "weather_condition": "Sunny",
            "source": "Open-Meteo",
            "field_id": field_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_soil_analysis(
    client: TestClient,
    token: str,
    field_id: int,
) -> dict:
    response = client.post(
        "/api/v1/soil-analyses/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "analysis_date": "2026-07-26",
            "ph": 6.8,
            "nitrogen": 18.5,
            "phosphorus": 12.3,
            "potassium": 20.1,
            "organic_matter": 2.8,
            "moisture": 35.0,
            "laboratory": "BACA Lab",
            "recommendations": "Ajouter un engrais azoté",
            "field_id": field_id,
        },
    )

    assert response.status_code == 201

    return response.json()
