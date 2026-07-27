from app.schemas.recommendation import Recommendation


def irrigation_rule(weather):
    recommendations = []

    if weather.rainfall > 5:
        recommendations.append("Irrigation non nécessaire : pluie suffisante prévue.")

    elif weather.temperature_max > 32 and weather.humidity < 50:
        recommendations.append(
            "Irrigation recommandée : forte température et faible humidité."
        )

    else:
        recommendations.append("Surveiller l'humidité du sol avant irrigation.")

    return recommendations


def disease_risk_rule(weather):
    recommendations = []

    if weather.humidity > 80 and weather.rainfall > 0:
        recommendations.append(
            "Risque élevé de maladies fongiques : surveiller les cultures."
        )

    return recommendations


def fertilizer_rule(soil):
    recommendations = []

    if soil.nitrogen < 20:
        recommendations.append(
            Recommendation(
                category="fertilization",
                priority="medium",
                title="Azote faible",
                description="La teneur en azote est inférieure au seuil recommandé.",
                action="Prévoir un apport azoté adapté.",
            )
        )

    if soil.ph < 6:
        recommendations.append("Sol acide : prévoir une correction du pH.")

    return recommendations


def crop_health_rule(crop, soil):
    recommendations = []

    if crop.name.lower() == "tomate":

        if soil.ph > 7.8:
            recommendations.append(
                "Tomate : sol alcalin détecté. "
                "Risque de blocage du fer. "
                "Contrôler le pH et envisager un apport de fer chélaté."
            )

        if soil.nitrogen < 20:
            recommendations.append(
                "Tomate : azote faible. " "Prévoir une fertilisation azotée adaptée."
            )

        if soil.moisture < 30:
            recommendations.append(
                "Tomate : humidité du sol faible. " "Vérifier l'irrigation."
            )

    return recommendations
