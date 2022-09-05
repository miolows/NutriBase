from dataclasses import dataclass
from dataclasses import InitVar


@dataclass
class FoodProduct:
    fp_id: int = 0
    category: str = ''
    description: str = ''


@dataclass
class Nutrient:
    n_id: int = 0
    name: str = ''
    unit: str = ''    


@dataclass
class NutritionDeclaration:
    nd_id: int = 0
    food_ref: int = 0
    nutrient_ref: int = 0
    value: float = 0.0