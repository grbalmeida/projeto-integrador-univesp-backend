import psycopg2
import psycopg2.extras
import os

# localhost
# hub_solidario_desenvolvimento
# postgres
# default_123

class Repository:
    table_name = None
    primary_key = None
    connection = None
    cur = None

    def __init__(self, table_name, primary_key):
        self.table_name = table_name
        self.primary_key = primary_key

        self.connection = psycopg2.connect(
            host=os.environ.get('DATABASE_HOST'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD')
        )

        self.cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def obter_todos(self):
        self.cur.execute(f'select * from {self.table_name}')
        entities = self.cur.fetchall()
        return entities

    def obter(self, id):
        self.cur.execute(f'select * from {self.table_name} where {self.primary_key} = {id}')
        entity = self.cur.fetchone()
        return entity

    def __del__(self):
        self.cur.close()
        self.connection.close()