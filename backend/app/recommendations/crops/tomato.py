def tomato_rules(crop, soil):

    recommendations = []

    if crop.name == "tomato":

        if soil.ph > 7.8:
            recommendations.append(
                "Tomate : risque de blocage du fer en sol alcalin. "
                "Contrôler le pH et envisager un apport de fer chélaté."
            )

        if soil.nitrogen < 20:
            recommendations.append(
                "Tomate : azote faible, prévoir une fertilisation adaptée."
            )

    return recommendations
