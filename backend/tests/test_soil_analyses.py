def test_get_analyses_without_login(client):
    response = client.get("/api/v1/soil-analyses/")

    assert response.status_code == 401


def test_get_analyses_authenticated(client, token):
    response = client.get(
        "/api/v1/soil-analyses/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_analysis(soil_analysis, field):
    assert soil_analysis["field_id"] == field["id"]
    assert soil_analysis["ph"] == 6.8
    assert soil_analysis["laboratory"] == "BACA Lab"


def test_get_analysis_by_id(client, token, soil_analysis):
    response = client.get(
        f"/api/v1/soil-analyses/{soil_analysis['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == soil_analysis["id"]
    assert data["ph"] == 6.8
    assert data["laboratory"] == "BACA Lab"


def test_update_analysis(client, token, soil_analysis):
    response = client.put(
        f"/api/v1/soil-analyses/{soil_analysis['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "ph": 7.2,
            "recommendations": "Ajouter du compost",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ph"] == 7.2
    assert data["recommendations"] == "Ajouter du compost"


def test_delete_analysis(client, token, soil_analysis):
    response = client.delete(
        f"/api/v1/soil-analyses/{soil_analysis['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/soil-analyses/{soil_analysis['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
