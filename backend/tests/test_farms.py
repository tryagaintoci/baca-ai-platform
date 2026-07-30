from tests.helpers import get_token


def test_get_farms_authenticated(client, token):
    response = client.get(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_farm(client, token):
    response = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Ferme pytest",
            "location": "Blida",
        },
    )

    assert response.status_code == 201

    farm = response.json()

    assert farm["name"] == "Ferme pytest"
    assert farm["location"] == "Blida"
    assert "id" in farm
    assert "owner_id" in farm


def test_get_farm_by_id(client, token):
    create = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Ferme Test",
            "location": "Alger",
        },
    )

    assert create.status_code == 201

    farm_id = create.json()["id"]

    response = client.get(
        f"/api/v1/farms/{farm_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    farm = response.json()

    assert farm["id"] == farm_id
    assert farm["name"] == "Ferme Test"


def test_update_farm(client, token):
    create = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Old Farm",
            "location": "Blida",
        },
    )

    assert create.status_code == 201

    farm_id = create.json()["id"]

    response = client.put(
        f"/api/v1/farms/{farm_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "New Farm",
            "location": "Oran",
        },
    )

    assert response.status_code == 200

    farm = response.json()

    assert farm["name"] == "New Farm"
    assert farm["location"] == "Oran"


def test_delete_farm(client, token):
    create = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Delete Farm",
            "location": "Tizi Ouzou",
        },
    )

    assert create.status_code == 201

    farm_id = create.json()["id"]

    response = client.delete(
        f"/api/v1/farms/{farm_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/farms/{farm_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_get_farm_forbidden(client):
    ahmed_token = get_token(client, "ahmed@example.com", "Baca123!")
    ali_token = get_token(client, "ali@example.com", "Baca123!")

    create = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {ahmed_token}"},
        json={
            "name": "Private Farm",
            "location": "Alger",
        },
    )

    assert create.status_code == 201

    farm_id = create.json()["id"]

    response = client.get(
        f"/api/v1/farms/{farm_id}",
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    assert response.status_code == 403


def test_get_farm_not_found(client, token):
    response = client.get(
        "/api/v1/farms/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
