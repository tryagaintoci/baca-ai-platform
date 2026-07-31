def test_get_weather_without_login(client):
    response = client.get("/api/v1/weather/")

    assert response.status_code == 401


def test_get_weather_authenticated(client, token):
    response = client.get(
        "/api/v1/weather/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_weather(weather, field):
    assert weather["field_id"] == field["id"]
    assert weather["temperature_min"] == 18.5
    assert weather["temperature_max"] == 31.2
    assert weather["weather_condition"] == "Sunny"
    assert weather["source"] == "Open-Meteo"


def test_get_weather_by_id(client, token, weather):
    response = client.get(
        f"/api/v1/weather/{weather['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather["id"]
    assert data["temperature_min"] == 18.5
    assert data["weather_condition"] == "Sunny"


def test_update_weather(client, token, weather):
    response = client.put(
        f"/api/v1/weather/{weather['id']}",
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


def test_delete_weather(client, token, weather):
    response = client.delete(
        f"/api/v1/weather/{weather['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/weather/{weather['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
