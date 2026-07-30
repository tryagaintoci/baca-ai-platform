from app.schemas.recommendation import Recommendation


def irrigation_rule(weather):
    recommendations = []

    if weather.rainfall > 5:
        recommendations.append(
            Recommendation(
                category="irrigation",
                priority="low",
                title="Irrigation non nécessaire",
                description="La pluie prévue est suffisante.",
                action="Aucune irrigation n'est nécessaire aujourd'hui.",
            )
        )

    elif weather.temperature_max > 32 and weather.humidity < 50:
        recommendations.append(
            Recommendation(
                category="irrigation",
                priority="high",
                title="Irrigation recommandée",
                description="Température élevée et faible humidité.",
                action="Irriguer de préférence tôt le matin ou en soirée.",
            )
        )

    else:
        recommendations.append(
            Recommendation(
                category="irrigation",
                priority="medium",
                title="Surveillance de l'irrigation",
                description="Les conditions sont normales.",
                action="Vérifier l'humidité du sol avant d'irriguer.",
            )
        )

    return recommendations


def disease_risk_rule(weather):
    recommendations = []

    if weather.humidity > 80 and weather.rainfall > 0:
        recommendations.append(
            Recommendation(
                category="disease",
                priority="high",
                title="Risque de maladie",
                description="Humidité élevée avec pluie prévue.",
                action="Surveiller les cultures et envisager un traitement préventif.",
            )
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
        recommendations.append(
            Recommendation(
                category="soil",
                priority="medium",
                title="Sol acide",
                description="Le pH du sol est inférieur à 6.",
                action="Prévoir un amendement pour corriger le pH.",
            )
        )

    return recommendations


def crop_health_rule(crop, soil):
    recommendations = []

    if crop.name.lower() == "tomate":
        if soil.ph > 7.8:
            recommendations.append(
                Recommendation(
                    category="crop",
                    priority="high",
                    title="Sol alcalin",
                    description="Risque de blocage du fer.",
                    action="Contrôler le pH et prévoir un apport de fer chélaté.",
                )
            )

        if soil.nitrogen < 20:
            recommendations.append(
                Recommendation(
                    category="crop",
                    priority="medium",
                    title="Azote faible",
                    description="La tomate présente un besoin en azote.",
                    action="Prévoir une fertilisation azotée.",
                )
            )

        if soil.moisture < 30:
            recommendations.append(
                Recommendation(
                    category="crop",
                    priority="high",
                    title="Humidité insuffisante",
                    description="Le sol est trop sec pour la culture de tomate.",
                    action="Vérifier immédiatement l'irrigation.",
                )
            )

    return recommendations
