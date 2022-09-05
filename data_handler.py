import pandas as pd
from tqdm import tqdm


from usda import USDA
from food import *

'''
def sort_products(data):
    product_cat = list(set([d.get('foodCategory') for d in data]))
    product_classifier = {p_c: list() for p_c in product_cat}
    for product in data:
        cat = product.get('foodCategory')
        product_classifier.get(cat).append(product)
    return product_classifier

def data_tables(foods_data):
    food_products = []
    food_nutriens = []
    for product_data in tqdm(foods_data):
        fp = food_product(product_data)
        fn = food_nutrients(product_data.get('foodNutrients'), fp.fdc_id)
        food_products.append(fp)
        food_nutriens += fn
    return food_products, food_nutriens

def food_product(product_data):
    fdc_id = product_data.get('fdcId')
    cat = product_data.get('foodCategory')
    name = product_data.get('description')
    fp = FoodProduct(fdc_id, cat, name)
    return fp


def food_nutrients(nutrients_data, food_id):
    food_nutrients = []
    for nutrient_data in nutrients_data:
        n_id = nutrient_data.get('foodNutrientId')
        n_name = nutrient_data.get('nutrientName')
        n_unit = nutrient_data.get('unitName')
        n_value = nutrient_data.get('value')
        n = Nutrient(n_id, food_id, n_name, n_unit, n_value)
        food_nutrients.append(n)
    return food_nutrients
'''

''' ----------------------------------------------------------------------- '''

def data_tables(foods_data):
    f_products = []
    nutrients = []
    n_declarations = []
    
    for fd in tqdm(foods_data):
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



# def data_tables(foods_data):
#     fp = [food_product(p) for p in tqdm(foods_data)]
#     fnh = [[nutrients_data_holder(p.get('fdcId'), n) for n in p.get('foodNutrients')] 
#            for p in tqdm(foods_data)]
    
#     fp = pd.DataFrame(fp)
#     fnh = pd.DataFrame(fnh)
#     return fp, fnh





if __name__ == '__main__':
    usda_data = USDA('key.txt')
    raw = usda_data.get_food_data('SR Legacy')
    foods, nutrients, declarations = data_tables(raw)