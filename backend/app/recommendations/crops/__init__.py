from app.recommendations.crops.maize import maize_rules
from app.recommendations.crops.tomato import tomato_rules

CROP_RULES = {
    "maïs": maize_rules,
    "mais": maize_rules,
    "corn": maize_rules,
    "tomate": tomato_rules,
    "tomato": tomato_rules,
}
