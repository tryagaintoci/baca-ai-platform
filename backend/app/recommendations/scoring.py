from app.models.crop import Crop
from app.models.soil_analysis import SoilAnalysis
from app.models.weather import Weather


def calculate_health_score(
    weather: Weather,
    soil: SoilAnalysis,
    crop: Crop,
) -> int:
    score = 100

    # Température
    if weather.temperature_max > 35:
        score -= 10

    # Humidité
    if weather.humidity < 40:
        score -= 10

    # Azote
    if soil.nitrogen < 20:
        score -= 10

    # pH
    if soil.ph < 6:
        score -= 10

    # Matière organique
    if soil.organic_matter < 2:
        score -= 5

    # La variable crop est réservée pour les futures règles
    _ = crop

    return max(score, 0)


def calculate_risk_level(score: int) -> str:
    if score >= 90:
        return "LOW"

    if score >= 70:
        return "MEDIUM"

    if score >= 50:
        return "HIGH"

    return "CRITICAL"