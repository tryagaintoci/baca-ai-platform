from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

FIELD_ID = 2


def get_token():
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "ahmed@example.com",
            "password": "Baca123!",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_weather(token):
    response = client.post(
        "/api/v1/weather/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "forecast_date": "2026-07-27",
            "temperature_min": 18.5,
            "temperature_max": 31.2,
            "humidity": 68.0,
            "rainfall": 1.5,
            "wind_speed": 12.4,
            "weather_condition": "Sunny",
            "source": "Open-Meteo",
            "field_id": FIELD_ID,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_get_weather_without_login():
    response = client.get("/api/v1/weather/")

    assert response.status_code == 401


def test_get_weather_authenticated():
    token = get_token()

    response = client.get(
        "/api/v1/weather/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_weather():
    token = get_token()

    weather = create_weather(token)

    assert weather["field_id"] == FIELD_ID
    assert weather["temperature_min"] == 18.5
    assert weather["temperature_max"] == 31.2
    assert weather["weather_condition"] == "Sunny"
    assert weather["source"] == "Open-Meteo"


def test_get_weather_by_id():
    token = get_token()

    weather = create_weather(token)
    weather_id = weather["id"]

    response = client.get(
        f"/api/v1/weather/{weather_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather_id
    assert data["temperature_min"] == 18.5
    assert data["weather_condition"] == "Sunny"


def test_update_weather():
    token = get_token()

    weather = create_weather(token)
    weather_id = weather["id"]

    response = client.put(
        f"/api/v1/weather/{weather_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "temperature_max": 35.0,
            "weather_condition": "Hot",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["temperature_max"] == 35.0
    assert data["weather_condition"] == "Hot"


def test_delete_weather():
    token = get_token()

    weather = create_weather(token)
    weather_id = weather["id"]

    response = client.delete(
        f"/api/v1/weather/{weather_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/weather/{weather_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
