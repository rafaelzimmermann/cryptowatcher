from model.balance import Balance
from model.portfolio import Portfolio
from storage.transactionstorage import TransactionStorage
from price.priceservice import PriceService


class BalanceCalculator:

    def __init__(self, storage: TransactionStorage, price_service: PriceService):
        self.storage = storage
        self.price_service = price_service

    def calculate_from_beginning(self) -> Portfolio:
        portfolio = Portfolio(self.price_service)
        portfolio.add_transactions(self.storage.all_transactions())
        return portfolio

    def get_transactions(self, limit: int = 25, offset: int = 0):
        return self.storage.get_transactions(limit, offset)
