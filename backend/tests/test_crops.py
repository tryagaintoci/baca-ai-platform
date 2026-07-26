from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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


def create_crop(token):
    response = client.post(
        "/api/v1/crops/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Maïs",
            "variety": "Hybrid",
            "planting_date": "2026-09-01",
            "expected_harvest_date": "2027-01-15",
            "status": "Growing",
            "season": "2026",
            "notes": "Test pytest",
            "field_id": 2,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_get_crops_without_login():
    response = client.get("/api/v1/crops/")

    assert response.status_code == 401


def test_get_crops_authenticated():
    token = get_token()

    response = client.get(
        "/api/v1/crops/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_crop():
    token = get_token()

    crop = create_crop(token)

    assert crop["name"] == "Maïs"
    assert crop["variety"] == "Hybrid"
    assert crop["status"] == "Growing"
    assert crop["field_id"] == 2


def test_get_crop_by_id():
    token = get_token()

    crop = create_crop(token)
    crop_id = crop["id"]

    response = client.get(
        f"/api/v1/crops/{crop_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == crop_id
    assert data["name"] == "Maïs"
    assert data["variety"] == "Hybrid"


def test_update_crop():
    token = get_token()

    crop = create_crop(token)
    crop_id = crop["id"]

    response = client.put(
        f"/api/v1/crops/{crop_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "Harvested", "notes": "Récolte terminée"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Harvested"
    assert data["notes"] == "Récolte terminée"


def test_delete_crop():
    token = get_token()

    crop = create_crop(token)
    crop_id = crop["id"]

    response = client.delete(
        f"/api/v1/crops/{crop_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/crops/{crop_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
