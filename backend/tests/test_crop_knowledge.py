from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_crop_knowledge():
    response = client.get("/api/v1/knowledge/crops/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_crop_knowledge():
    crop_name = f"Maïs-{uuid4().hex[:8]}"

    response = client.post(
        "/api/v1/knowledge/crops/",
        json={
            "common_name": crop_name,
            "scientific_name": "Zea mays",
            "family": "Poaceae",
            "description": "Culture céréalière",
            "optimal_ph_min": 5.8,
            "optimal_ph_max": 7.2,
            "min_temperature": 18,
            "max_temperature": 35,
            "water_requirement": "Élevé",
            "growth_duration_days": 120,
            "source": "FAO",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["common_name"] == crop_name
    assert data["scientific_name"] == "Zea mays"
    assert "id" in data


def test_get_crop_by_name():
    crop_name = f"Maïs-{uuid4().hex[:8]}"

    create_response = client.post(
        "/api/v1/knowledge/crops/",
        json={
            "common_name": crop_name,
            "scientific_name": "Zea mays",
            "family": "Poaceae",
            "description": "Culture céréalière",
            "optimal_ph_min": 5.8,
            "optimal_ph_max": 7.2,
            "min_temperature": 18,
            "max_temperature": 35,
            "water_requirement": "Élevé",
            "growth_duration_days": 120,
            "source": "FAO",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/api/v1/knowledge/crops/{crop_name}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["common_name"] == crop_name
    assert data["scientific_name"] == "Zea mays"


def test_crop_not_found():
    response = client.get("/api/v1/knowledge/crops/CultureInexistante12345")

    assert response.status_code == 404
