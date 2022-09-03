import pandas as pd

from usda import USDA
from data_handler import data_tables
from nutri_base import NutriBase


if __name__ == '__main__':
    usda_api_key_file = 'key.txt'
    sql_password_file = "mysqlpw.txt"
    
    usda_data = USDA(usda_api_key_file)
    food_data = usda_data.get_food_data('SR Legacy')
    food, nutrients = data_tables(food_data)
    
    food_df = pd.DataFrame(food)
    nutri_df = pd.DataFrame(nutrients)
    
    nutri_base = NutriBase(sql_password_file)
    
    nutri_base.create_tabs()
    nutri_base.add_data('food_product', food_df)
    nutri_base.add_data('nutrient', nutri_df)