from model.balance import Balance
from model.portfolio import Portfolio
from storage.transactionstorage import TransactionStorage
from storage.portifoliostorage import PortifolioStorage


class BalanceCalculator:

    def __init__(self, storage: TransactionStorage):
        self.storage = storage

    def calculate_from_beginning(self) -> Portfolio:
        portfolio = Portfolio()
        portfolio.add_transactions(self.storage.all_transactions())
        return portfolio

    def get_transactions(self, limit: int = 25, offset: int = 0):
        return self.storage.get_transactions(limit, offset)
