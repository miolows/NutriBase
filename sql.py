import mysql.connector
from mysql.connector import Error
import pandas as pd
from tqdm import tqdm


class DataBase():
    def __init__(self, data_base_name, user_password_file, host_name='localhost', user_name='root'):
        self.host = host_name
        self.user = user_name
        self.db = data_base_name
        with open(user_password_file, 'r') as pf:
            self.password = pf.read()
        
        self.db_connection = self.set_database_connection(self.db)
        
        
    def set_database_connection(self, db_name):
        dc = self.database_connection(db_name)
        if dc is None:
            sc = self.server_connection()
            self.create_database(sc, db_name)
            dc = self.database_connection(db_name)
        return dc

    def server_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        passwd = self.password
            )
            print("MySQL server connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection
    
    
    def database_connection(self, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        passwd = self.password,
                        database = db_name
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection
    
    
    def create_database(self, connection, db_name):
        cursor = connection.cursor()
        try:
            query = f'CREATE DATABASE {db_name}'
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")
            
            
    def execute_query(self, query):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query)
            self.db_connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
            
    
    def execute_list_query(self, sql, val):
        cursor = self.db_connection.cursor()
        try:
            cursor.executemany(sql, val)
            self.db_connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
            
            
    def read_query(self, query):
        cursor = self.db_connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
            
            
    def lread_query(self, query):
        cursor = self.db_connection.cursor()
        result = None
        try:
            cursor.execute(query)
            columns = cursor.description 
            result = [{columns[index][0]:column for index, column in 
                       enumerate(value)} for value in cursor.fetchall()]
            return result
        except Error as err:
            print(f"Error: '{err}'")
            
            
    def create_table(self, name, fields, types, details):
        sql_lines = ', '.join([f'{f} {t} {d}' for f, t, d in zip(fields, types, details)])
        query = f'CREATE TABLE IF NOT EXISTS {name} ({sql_lines});'
        self.execute_query(query)
            
    def alter_table(self, table, foreign_key, reference_table, reference_field, on_delete):
        query = f'''
        ALTER TABLE {table}
        ADD FOREIGN KEY({foreign_key})
        REFERENCES {reference_table}({reference_field})
        ON DELETE {on_delete};
        '''
        self.execute_query(query)
        
    def show_tables(self):
        return [tab[0] for tab in self.read_query('SHOW TABLES;')]
    
    def add_data(self, table_name, data_frame):
        cols = data_frame.columns.tolist()
        cols_query = ', '.join(cols)
        rows_query = ', '.join(['%s']*len(cols))
        
        sql_query = f'INSERT INTO {table_name} ({cols_query}) VALUES ({rows_query})'
        values = [tuple(row) for i, row in tqdm(data_frame.iterrows())]
        self.execute_list_query(sql_query, values)



    # def create_table(self, connection, table_name, pandas_df, primary_key_index=0):
    #     type_to_sql = {'int64': 'INT', 'int32': 'INT', 'float64': 'FLOAT', 'bool': 'BOOLEAN'}
    #     field_names = list(pandas_df.columns.values)
    #     field_types = [type_to_sql.get(str(i), 'VARCHAR(40)') for i in list(pandas_df.dtypes)]
    #     lines = []
    #     for i, f in enumerate(zip(field_names, field_types)):
    #         line = " ".join(f)
    #         if i == primary_key_index:
    #             line += " PRIMARY KEY, "
    #         else:
    #             line += ", "
    #         lines.append(line)
        
    #     query = f'CREATE TABLE IF NOT EXISTS {table_name}({"".join(lines)});'
    #     self.execute_query(connection, query)