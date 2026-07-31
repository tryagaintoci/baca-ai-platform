from types import SimpleNamespace

from app.recommendations.engine import RecommendationEngine


def test_generate_for_tomato():
    weather = SimpleNamespace(
        rainfall=0,
        temperature_max=36,
        humidity=35,
    )

    soil = SimpleNamespace(
        nitrogen=10,
        ph=8.0,
        moisture=20,
        organic_matter=2.5,
    )

    crop = SimpleNamespace(
        name="Tomate",
    )

    engine = RecommendationEngine()

    recommendations = engine.generate(
        weather,
        soil,
        crop,
    )

    assert len(recommendations) > 0


def test_generate_for_unknown_crop():
    weather = SimpleNamespace(
        rainfall=0,
        temperature_max=25,
        humidity=70,
    )

    soil = SimpleNamespace(
        nitrogen=25,
        ph=6.8,
        moisture=40,
        organic_matter=3,
    )

    crop = SimpleNamespace(
        name="UnknownCrop",
    )

    engine = RecommendationEngine()

    recommendations = engine.generate(
        weather,
        soil,
        crop,
    )

    assert isinstance(recommendations, list)