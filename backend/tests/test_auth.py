def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_login_valid_credentials(client):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "ahmed@example.com",
            "password": "Baca123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user(client):
    login = client.post(
        "/api/v1/auth/token",
        data={
            "username": "ahmed@example.com",
            "password": "Baca123!",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    user = response.json()

    assert user["email"] == "ahmed@example.com"


def test_login_ali(client):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "ali@example.com",
            "password": "Baca123!",
        },
    )

    assert response.status_code == 200
