import concurrent.futures
import requests
import pandas as pd
from tqdm import tqdm

from food import *

class USDA():
    def __init__(self, api_key_file):
        self.main_url = 'https://api.nal.usda.gov/fdc/v1'
        with open(api_key_file, 'r') as f:
            self.key = f.read()
            

    def encode_dtype(self, db):
        type_string = {'Branded': 'Branded',
                       'Foundation': 'Foundation',
                       'Survey (FNDDS)': 'Survey%20%28FNDDS%29',
                       'Survey': 'Survey%20%28FNDDS%29',
                       'FNDDS':'Survey%20%28FNDDS%29',
                       'SR Legacy': 'SR%20Legacy',
                       'All': 'Branded,Foundation,Survey%20%28FNDDS%29,SR%20Legacy'}
        return type_string.get(db, type_string.get('All'))

    def food_item(self, food_id, nutrients=[], data_format='full'):
        n = '&'.join([f'nutrients={i}' for i in nutrients])
        url = f'{self.main_url}/food/{food_id}?format={data_format}&{n}&api_key={self.key}'
        api_response = requests.get(url)
        return api_response.json()

    def food_items(self, food_ids, nutrients=[], data_format='full'):
        fid = '&'.join([f'fdcIds={i}' for i in food_ids])
        n = '&'.join([f'nutrients={i}' for i in nutrients])
        url = f'{self.main_url}/foods?{fid}&format={data_format}&{n}&api_key={self.key}'
        api_response = requests.get(url)
        return api_response.json()
    
    def food_list(self, data_type, page_num=1, page_size=50):
        dt = self.encode_dtype(data_type)
        url = f'{self.main_url}/foods/list?dataType={dt}&pageSize={page_size}&pageNumber={page_num}&api_key={self.key}'
        api_response = requests.get(url)
        return api_response.json()

    def food_search(self, data_type, page_num=1, food_name='', brand_owner='', page_size=50):
        dt = self.encode_dtype(data_type)
        fnstr = food_name.replace(' ', '%20')
        bostr = brand_owner.replace(' ', '%20')
        url = f'{self.main_url}/foods/search?query={fnstr}&brandOwner={bostr}&dataType={dt}&pageSize={page_size}&pageNumber={page_num}&api_key={self.key}'
        api_response = requests.get(url)
        return api_response.json()
    
    
    def get_food_data(self, data_type):
        first_page = self.food_search(data_type)
        total_pages = first_page.get('totalPages')
        food_data = first_page.get('foods')
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.food_search, data_type, page) 
                       for page in range(2, total_pages+1)]
            
            for r in tqdm(concurrent.futures.as_completed(results), total=total_pages-1):
                n_page = r.result()
                n_data = n_page.get('foods')
                food_data += n_data
            
        return food_data
    
    
    def sort_data(self, food_data):
        f_products = []
        nutrients = []
        n_declarations = []
        
        for fd in tqdm(food_data):
            fp_id = fd.get('fdcId')
            cat = fd.get('foodCategory')
            desc = fd.get('description')
            fd_nutrient_data = fd.get('foodNutrients')
            f_products.append(FoodProduct(fp_id, cat, desc))
            
            for fn in fd_nutrient_data:
                n_id = fn.get('nutrientId')
                nd_id = fn.get('foodNutrientId')
                name = fn.get('nutrientName')
                unit = fn.get('unitName')
                value = fn.get('value')
                
                nutrients.append(Nutrient(n_id, name, unit))
                n_declarations.append(NutritionDeclaration(nd_id, fp_id, n_id, value))
                
        f_products = pd.DataFrame(f_products)
        nutrients = pd.DataFrame(nutrients).drop_duplicates()
        n_declarations = pd.DataFrame(n_declarations)
        
        return f_products, nutrients, n_declarations

if __name__ == '__main__':    
    u = USDA('key.txt')
    x = u.get_food_data('SR Legacy')