from unittest.mock import patch


def test_sync_weather(
    client,
    token,
    field,
):
    fake_response = {
        "daily": {
            "time": [
                "2026-08-01",
                "2026-08-02",
            ],
            "temperature_2m_min": [
                18.0,
                19.0,
            ],
            "temperature_2m_max": [
                30.0,
                31.0,
            ],
            "precipitation_sum": [
                0.5,
                2.0,
            ],
            "windspeed_10m_max": [
                12.0,
                15.0,
            ],
            "relative_humidity_2m_mean": [
                65,
                72,
            ],
            "weathercode": [
                0,
                3,
            ],
        }
    }

    with patch(
        "app.services.weather_service.OpenMeteoClient.get_forecast",
        return_value=fake_response,
    ):
        response = client.post(
            f"/api/v1/weather/sync/{field['id']}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["field_id"] == field["id"]
    assert data[0]["temperature_min"] == 18.0
    assert data[0]["temperature_max"] == 30.0
    assert data[0]["source"] == "Open-Meteo"

    assert data[1]["field_id"] == field["id"]
    assert data[1]["temperature_min"] == 19.0
    assert data[1]["temperature_max"] == 31.0
    assert data[1]["source"] == "Open-Meteo"