import psycopg2


class Database:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self._connection = psycopg2.connect(
            database="walletwatcher",
            user="walletwatcher",
            password="walletwatcher",
            host="postgres",
            port="5432")

    @property
    def connection(self):
        return self._connection

