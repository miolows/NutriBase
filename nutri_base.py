from sql import DataBase

class NutriBase(DataBase):
    def __init__(self, user_password_file):
        super().__init__('NutriBase', user_password_file)
        self.create_tables()
        self.alter_tables()
    
        
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
