from types import SimpleNamespace

from app.recommendations.rules import (
    crop_health_rule,
    disease_risk_rule,
    fertilizer_rule,
    irrigation_rule,
)


def test_irrigation_rule_rain():
    weather = SimpleNamespace(
        rainfall=10,
        temperature_max=25,
        humidity=70,
    )

    recommendations = irrigation_rule(weather)

    assert len(recommendations) == 1
    assert recommendations[0].category == "irrigation"
    assert recommendations[0].priority == "low"


def test_irrigation_rule_hot():
    weather = SimpleNamespace(
        rainfall=0,
        temperature_max=35,
        humidity=30,
    )

    recommendations = irrigation_rule(weather)

    assert recommendations[0].priority == "high"


def test_irrigation_rule_normal():
    weather = SimpleNamespace(
        rainfall=0,
        temperature_max=25,
        humidity=60,
    )

    recommendations = irrigation_rule(weather)

    assert recommendations[0].priority == "medium"


def test_disease_rule():
    weather = SimpleNamespace(
        humidity=90,
        rainfall=5,
    )

    recommendations = disease_risk_rule(weather)

    assert len(recommendations) == 1
    assert recommendations[0].category == "disease"


def test_fertilizer_rule():
    soil = SimpleNamespace(
        nitrogen=15,
        ph=5.5,
    )

    recommendations = fertilizer_rule(soil)

    assert len(recommendations) == 2


def test_crop_health_rule():
    crop = SimpleNamespace(
        name="Tomate",
    )

    soil = SimpleNamespace(
        ph=8.0,
        nitrogen=10,
        moisture=20,
    )

    recommendations = crop_health_rule(
        crop,
        soil,
    )

    assert len(recommendations) == 3