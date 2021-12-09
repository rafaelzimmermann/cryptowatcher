from model.balance import Balance
from model.portfolio import Portfolio
from storage.transactionstorage import TransactionStorage


class BalanceCalculator:

    def __init__(self, storage: TransactionStorage):
        self.storage = storage

    def calculate_from_beginning(self) -> Portfolio:
        portfolio = Portfolio()
        portfolio.add_transactions(self.storage.all_transactions())
        return portfolio
