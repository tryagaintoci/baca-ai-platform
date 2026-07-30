from app.recommendations.crops import CROP_RULES
from app.recommendations.rules import (
    crop_health_rule,
    disease_risk_rule,
    fertilizer_rule,
    irrigation_rule,
)


class RecommendationEngine:
    def generate(
        self,
        weather,
        soil,
        crop,
    ):
        recommendations = []

        # Règles générales
        recommendations.extend(irrigation_rule(weather))
        recommendations.extend(disease_risk_rule(weather))
        recommendations.extend(fertilizer_rule(soil))
        recommendations.extend(crop_health_rule(crop, soil))

        # Règles spécifiques à la culture
        crop_rule = CROP_RULES.get(
            crop.name.lower(),
        )

        if crop_rule:
            recommendations.extend(crop_rule(weather, soil, crop))

        return recommendations
