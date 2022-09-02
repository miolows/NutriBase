from sql import DataBase

class NutriBase(DataBase):
    def __init__(self, user_password_file):
        super().__init__('NutriBase', user_password_file)
    
        
    def create_tabs(self):
        self.create_table('food_product',
                          ['fdc_id', 'category', 'description'],
                          ['INT', 'VARCHAR(40)', 'VARCHAR(40)'],
                          ['PRIMARY KEY', 'NOT NULL', 'NOT NULL'])
        
        self.create_table('nutrient', 
                          ['nutrient_id', 'food', 'name', 'unit', 'value'],
                          ['INT', 'INT', 'VARCHAR(40)', 'VARCHAR(10)', 'FLOAT'],
                          ['PRIMARY KEY', 'NOT NULL', 'NOT NULL', 'NOT NULL', 'NOT NULL'])
        