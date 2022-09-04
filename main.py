import pandas as pd

from usda import USDA
from data_handler import data_tables
from nutri_base import NutriBase


if __name__ == '__main__':
    usda_api_key_file = 'key.txt'
    sql_password_file = "mysqlpw.txt"
    
    usda_data = USDA(usda_api_key_file)
    foods, nutrients, declarations = data_tables(usda_data.get_food_data('SR Legacy'))
    
    nutri_base = NutriBase(sql_password_file)
    
    nutri_base.add_data('food_product', foods)
    nutri_base.add_data('nutrient', nutrients)
    nutri_base.add_data('nutrition_declaration', declarations)
    
    