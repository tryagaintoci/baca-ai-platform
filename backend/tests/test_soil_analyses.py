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


def create_analysis(token):
    response = client.post(
        "/api/v1/soil-analyses/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "analysis_date": "2026-07-26",
            "ph": 6.8,
            "nitrogen": 18.5,
            "phosphorus": 12.3,
            "potassium": 20.1,
            "organic_matter": 2.8,
            "moisture": 35.0,
            "laboratory": "BACA Lab",
            "recommendations": "Ajouter un engrais azoté",
            "field_id": FIELD_ID,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_get_analyses_without_login():
    response = client.get("/api/v1/soil-analyses/")

    assert response.status_code == 401


def test_get_analyses_authenticated():
    token = get_token()

    response = client.get(
        "/api/v1/soil-analyses/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_analysis():
    token = get_token()

    analysis = create_analysis(token)

    assert analysis["field_id"] == FIELD_ID
    assert analysis["ph"] == 6.8
    assert analysis["laboratory"] == "BACA Lab"


def test_get_analysis_by_id():
    token = get_token()

    analysis = create_analysis(token)
    analysis_id = analysis["id"]

    response = client.get(
        f"/api/v1/soil-analyses/{analysis_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == analysis_id
    assert data["ph"] == 6.8
    assert data["laboratory"] == "BACA Lab"


def test_update_analysis():
    token = get_token()

    analysis = create_analysis(token)
    analysis_id = analysis["id"]

    response = client.put(
        f"/api/v1/soil-analyses/{analysis_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"ph": 7.2, "recommendations": "Ajouter du compost"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ph"] == 7.2
    assert data["recommendations"] == "Ajouter du compost"


def test_delete_analysis():
    token = get_token()

    analysis = create_analysis(token)
    analysis_id = analysis["id"]

    response = client.delete(
        f"/api/v1/soil-analyses/{analysis_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/soil-analyses/{analysis_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
