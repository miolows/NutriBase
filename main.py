from nutri_base import NutriBase


if __name__ == '__main__':
    usda_api_key_file = 'key.txt'
    sql_password_file = "mysqlpw.txt"
    nutri_base = NutriBase(sql_password_file, usda_api_key_file, 'SR Legacy')
    
    
    