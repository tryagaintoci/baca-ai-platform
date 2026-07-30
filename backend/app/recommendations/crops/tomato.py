from app.schemas.recommendation import Recommendation


def tomato_rules(weather, soil, crop):
    recommendations = []

    if soil.ph > 7.8:
        recommendations.append(
            Recommendation(
                category="crop",
                priority="high",
                title="Sol alcalin",
                description="Risque de blocage du fer pour la tomate.",
                action="Contrôler le pH et prévoir un apport de fer chélaté.",
            )
        )

    if soil.nitrogen < 20:
        recommendations.append(
            Recommendation(
                category="fertilization",
                priority="medium",
                title="Azote faible",
                description="La tomate présente un besoin en azote.",
                action="Prévoir une fertilisation azotée adaptée.",
            )
        )

    return recommendations
