from dataclasses import dataclass
from dataclasses import InitVar

@dataclass
class Nutrient:
    nutrient_id: int = 0
    food: int = 0
    name: str = ''
    unit: str = ''
    value: float = 0.0
    

@dataclass
class FoodProduct:
    fdc_id: int = 0
    category: str = ''
    description: str = ''




# @dataclass
# class FoodProduct:
#     fdc_id: int = 0
#     category: str = ''
#     text_data: InitVar[str] = ''
#     name: str = ''
#     description: str = ''
#     state: str = ''
    
    
#     def __post_init__(self, text_data):
#         text = text_data.split(', ', 2)
#         self.name = text.pop(0)
#         if len(text)>1:
#             self.state = text.pop(0)
#         self.description = ''.join(text)

    
    







'''
# class FoodProduct:
#     def __init__(self, usda):
#         self.fdc_id = usda.get('fdcId')
#         self.category = usda.get('foodCategory')
#         self.name = usda.get('description')
#         self.nutrients = self.set_nutrients(usda.get('foodNutrients'))
#     # fdc_id: intnutrients
#     # category: str 
#     # name: str
#     # details: str
#     # preparation_state: str
#     # nutrients: List[Nutrient]
    
#     def set_nutrients(self, nutrients_db):
#         food_nutrients = []
#         for nutrient_data in nutrients_db:
#             n_id = nutrient_data.get('nutrientId')
#             n_name = nutrient_data.get('nutrientName')
#             n_unit = nutrient_data.get('unitName')
#             n_value = nutrient_data.get('value')
#             n = Nutrient(n_id, self.fdc_id, n_name, n_unit, n_value)
#             food_nutrients.append(n)
#         return food_nutrients
    
#     def frame_nutrients(self):
#         for n in self.nutrients:
#             n.data_frame()
'''