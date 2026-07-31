def test_get_recommendations(
    client,
    token,
    field,
    crop,
    weather,
    soil_analysis,
):
    response = client.get(
        f"/api/v1/recommendations/field/{field['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == field["id"]
    assert data["crop"] == crop["name"]

    assert isinstance(data["health_score"], int)
    assert data["health_score"] >= 0

    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_get_recommendations_without_login(
    client,
    field,
):
    response = client.get(
        f"/api/v1/recommendations/field/{field['id']}"
    )

    assert response.status_code == 401