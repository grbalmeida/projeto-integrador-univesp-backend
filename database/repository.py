import psycopg2
import os

# localhost
# hub_solidario_desenvolvimento
# postgres
# default_123

class Repository:
    table_name = None
    connection = None
    cur = None

    def __init__(self, table_name):
        self.table_name = table_name
        self.connection = psycopg2.connect(
            host=os.environ.get('DATABASE_HOST'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD')
        )

        self.cur = self.connection.cursor()

    def obter_todos(self):
        self.cur.execute(f'select * from {self.table_name}')
        entities = self.cur.fetchall()
        return entities

    def __del__(self):
        self.cur.close()
        self.connection.close()