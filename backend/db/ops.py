import psycopg2

import os
from dotenv import load_dotenv

class PostgresOps:
    def __init__(self):
                
        load_dotenv()

        database = os.getenv("DB_NAME")
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        port = os.getenv("DB_PORT")

        self.conn = psycopg2.connect(database=database,
                        host=host,
                        user=user,
                        password=password,
                        port=port)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_with_types = ', '.join([f"{col} TEXT" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['%s'] * len(data))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def fetch_data(self, table_name):
        fetch_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()
    
    def update_data(self, table_name, set_values, condition):
        set_columns = ', '.join([f"{col}" for col in set_values.keys()])
        condition_str = ' AND '.join([f"{col}" for col in condition.keys()])
        update_query = f"UPDATE {table_name} SET {set_columns} WHERE {condition_str}"
        self.cursor.execute(update_query, list(set_values.values()) + list(condition.values()))
        self.conn.commit()

    def delete_data(self, table_name, condition):
        condition_str = ' AND '.join([f"{col}" for col in condition.keys()])
        delete_query = f"DELETE FROM {table_name} WHERE {condition_str}"
        self.cursor.execute(delete_query, list(condition.values()))
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()