from sql import DataBase
import pandas as pd
from usda import USDA
from data_handler import data_tables

class NutriBase(DataBase):
    def __init__(self, user_password_file, *args):
        super().__init__('NutriBase', user_password_file)
        if not self.check_tables():
            self.create_tables()
            self.alter_tables()
        if args:
            self.fill_tables(*args)
    
    def check_tables(self, tabs=['food_product', 'nutrient', 'nutrition_declaration']):
        sql_tabs = self.show_tables()
        same = set(sql_tabs) == set(tabs)
        return same   
    
    def fill_tables(self, usda_api_key_file, *usda):
        for usda_data_type in usda:
            usda_data = USDA(usda_api_key_file)
            foods, nutrients, declarations = data_tables(usda_data.get_food_data(usda_data_type))
            
            self.add_data('food_product', foods)
            self.add_data('nutrient', nutrients)
            self.add_data('nutrition_declaration', declarations)
        
        
    def create_tables(self):
        self.create_table('food_product',
                          ['fp_id', 'category', 'description'],
                          ['INT', 'VARCHAR(40)', 'VARCHAR(200)'],
                          ['PRIMARY KEY', 'NOT NULL', 'NOT NULL'])
        
        self.create_table('nutrient', 
                          ['n_id', 'name', 'unit'],
                          ['INT', 'VARCHAR(40)', 'VARCHAR(10)'],
                          ['PRIMARY KEY', 'NOT NULL', 'NOT NULL'])
        
        self.create_table('nutrition_declaration', 
                          ['nd_id', 'food_ref', 'nutrient_ref', 'value'],
                          ['INT', 'INT', 'INT', 'FLOAT'],
                          ['PRIMARY KEY', 'NOT NULL', 'NOT NULL', ''])
        
        
    def alter_tables(self):
        self.alter_table('nutrition_declaration', 'food_ref', 'food_product', 'fp_id', 'CASCADE')
        self.alter_table('nutrition_declaration', 'nutrient_ref', 'nutrient', 'n_id', 'CASCADE')

    def find(self, name, detail, category):
        query = f'''
        SELECT category, description
        FROM food_product
        WHERE description LIKE '{name}%{detail}%' AND category LIKE '{category}%';
        '''
        return pd.DataFrame(self.lread_query(query))
    
    def get_nutrients(self, food_id):
        query = f'''
        SELECT food_product.description, nutrition_declaration.value, nutrient.name, nutrient.unit
        FROM food_product
        JOIN nutrition_declaration ON nutrition_declaration.food_ref = food_product.fp_id
        JOIN nutrient ON nutrition_declaration.nutrient_ref = nutrient.n_id
        WHERE food_product.fp_id = {food_id}
        '''
        return pd.DataFrame(self.lread_query(query))