from enum import Enum


class GrowthStage(str, Enum):
    GERMINATION = "GERMINATION"
    VEGETATIVE = "VEGETATIVE"
    FLOWERING = "FLOWERING"
    FRUITING = "FRUITING"
    MATURITY = "MATURITY"
    HARVEST = "HARVEST"
