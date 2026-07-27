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

        recommendations.extend(irrigation_rule(weather))

        recommendations.extend(disease_risk_rule(weather))

        recommendations.extend(fertilizer_rule(soil))

        recommendations.extend(crop_health_rule(crop, soil))

        return recommendations
