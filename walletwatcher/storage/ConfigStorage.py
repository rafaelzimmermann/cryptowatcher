from storage.Database import Database
from model.config import Config


class ConfigStorage:

    def __init__(self, database: Database):
        self.database = database

    def update(self, configuration: Config):
        try:
            cursor = self.database.connection.cursor
            cursor.execute('INSERT INTO config (currency, manual_portifolio) VALUES (%s, %s)', (configuration.currency, configuration.to_json(),))
            self.connection.commit()
        except Exception as e:
            print('Failed to insert configuration:', configuration)
            print(e)