def test_get_crops_without_login(client):
    response = client.get("/api/v1/crops/")

    assert response.status_code == 401


def test_get_crops_authenticated(client, token):
    response = client.get(
        "/api/v1/crops/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_crop(crop):
    assert crop["name"] == "Maïs"
    assert crop["variety"] == "Hybrid"
    assert crop["status"] == "Growing"
    assert crop["growth_stage"] == "VEGETATIVE"


def test_get_crop_by_id(client, token, crop):
    response = client.get(
        f"/api/v1/crops/{crop['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == crop["id"]
    assert data["name"] == "Maïs"
    assert data["variety"] == "Hybrid"
    assert data["growth_stage"] == "VEGETATIVE"


def test_update_crop(client, token, crop):
    response = client.put(
        f"/api/v1/crops/{crop['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "status": "Harvested",
            "growth_stage": "HARVEST",
            "notes": "Récolte terminée",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Harvested"
    assert data["growth_stage"] == "HARVEST"
    assert data["notes"] == "Récolte terminée"


def test_delete_crop(client, token, crop):
    response = client.delete(
        f"/api/v1/crops/{crop['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/crops/{crop['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
