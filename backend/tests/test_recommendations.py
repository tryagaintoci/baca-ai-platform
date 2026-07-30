def test_get_recommendations(client, token, field, crop, weather, soil_analysis):
    response = client.get(
        f"/api/v1/recommendations/field/{field['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == field["id"]
    assert data["crop"] == "Maïs"
    assert isinstance(data["health_score"], int)
    assert isinstance(data["risk_level"], str)
    assert isinstance(data["recommendations"], list)


def test_recommendations_field_not_found(client, token):
    response = client.get(
        "/api/v1/recommendations/field/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


def test_recommendations_without_token(client):
    response = client.get(
        "/api/v1/recommendations/field/999999",
    )

    assert response.status_code == 401


def test_recommendations_invalid_token(client):
    response = client.get(
        "/api/v1/recommendations/field/999999",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
