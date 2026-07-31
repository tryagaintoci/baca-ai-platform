from app.schemas.recommendation import Recommendation


def maize_rules(weather, soil, crop):
    recommendations = []

    if soil.nitrogen < 30:
        recommendations.append(
            Recommendation(
                category="fertilization",
                priority="high",
                title="Azote insuffisant",
                description="Le maïs nécessite davantage d'azote.",
                action="Prévoir un apport d'engrais azoté.",
            )
        )

    if crop.growth_stage == "FLOWERING":
        recommendations.append(
            Recommendation(
                category="irrigation",
                priority="high",
                title="Besoin en eau critique",
                description=(
                    "Le maïs est en floraison, une humidité suffisante est essentielle."
                ),
                action="Maintenir une irrigation régulière.",
            )
        )

    elif crop.growth_stage == "MATURITY":
        recommendations.append(
            Recommendation(
                category="irrigation",
                priority="low",
                title="Réduction progressive de l'irrigation",
                description="Le maïs arrive à maturité.",
                action="Réduire progressivement les apports d'eau.",
            )
        )

    return recommendations
