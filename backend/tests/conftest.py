import os

os.environ["ENV_FILE"] = ".env.test"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import (
    create_crop,
    create_field,
    create_soil_analysis,
    create_weather,
    get_token,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    return get_token(client)


@pytest.fixture
def farm(client, token):
    response = client.post(
        "/api/v1/farms/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Farm pytest",
            "location": "Alger",
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def field(client, token, farm):
    return create_field(
        client,
        token,
        farm["id"],
    )


@pytest.fixture
def crop(client, token, field):

    return create_crop(
        client,
        token,
        field["id"],
    )


@pytest.fixture
def weather(client, token, field):
    return create_weather(
        client,
        token,
        field["id"],
    )


@pytest.fixture
def soil_analysis(client, token, field):
    return create_soil_analysis(
        client,
        token,
        field["id"],
    )
