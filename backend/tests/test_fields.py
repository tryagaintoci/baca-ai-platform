from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_fields(client, token):
    response = client.get(
        "/api/v1/fields/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_field(field):
    assert field["name"] == "Champ pytest"
    assert field["area_hectares"] == 12.5
    assert field["soil_type"] == "Argileux"
    assert "id" in field


def test_get_field_by_id(client, token, field):
    response = client.get(
        f"/api/v1/fields/{field['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == field["id"]
    assert response.json()["name"] == "Champ pytest"


def test_update_field(client, token, field):
    response = client.put(
        f"/api/v1/fields/{field['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Champ Modifié",
            "area_hectares": 20.0,
            "latitude": 35.5,
            "longitude": 2.5,
            "soil_type": "Sableux",
        },
    )

    assert response.status_code == 200

    updated = response.json()

    assert updated["name"] == "Champ Modifié"
    assert updated["area_hectares"] == 20.0
    assert updated["soil_type"] == "Sableux"


def test_delete_field(client, token, field):
    response = client.delete(
        f"/api/v1/fields/{field['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/fields/{field['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_get_field_not_found(client, token):
    response = client.get(
        "/api/v1/fields/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
