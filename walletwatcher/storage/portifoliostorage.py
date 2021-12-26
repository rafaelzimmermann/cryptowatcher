from storage.Database import Database

class PortifolioStorage:

    def __init__(self, database: Database) -> None:
        self.database = database

    def save(self, portfolio: str) -> None:
        try:
            connection = self.database.connection
            connection.cursor.execute('INSERT INTO portfolio (portfolio) VALUES (%s)', (portfolio,))
            connection.commit()
        except Exception as e:
            print('Failed to save portfolio', portfolio)
            print(e)
    
    def get(self) -> str:
        cursor = self.database.connection.cursor()
        cursor.execute('SELECT portfolio FROM portfolio')
        row = cursor.fetchone()
        if not row:
            return None
        return row[0]