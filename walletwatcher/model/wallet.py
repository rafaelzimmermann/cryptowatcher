from typing import List

from model.balance import Balance
from price.getprices import get_prices
from price.priceservice import PriceService

WALLET_EXODUS = 1
WALLET_BINANCE = 2
WALLET_CRYPTOCOM = 3
WALLET_DAEDALUS = 4

WALLETS = {
    1: 'Exodus',
    2: 'Binance',
    3: 'crypto.com',
    4: 'Daedalus'
}

WALLETS_PRECISION = {
    1: 8,
    2: 8,
    3: 8,
    4: 8
}

MIN_VAL = 1


class Wallet:

    def __init__(self, id: int, name: str, type: int, fiat: List[str] = ["EUR"]):
        # TODO drop mult fiat support
        self.id = id
        self.name = name
        self.type = type
        self.fiat = fiat
        self.balance = {}

    def deposit(self, ticker: str, amount: int):
        if ticker not in self.balance:
            self.balance[ticker] = Balance(ticker, amount, self.fiat)
        self.balance[ticker].amount += amount

    def adjust_balance(self, price_service: PriceService):
        tickers = [b.ticker for b in self.balance.values()]
        prices = {p.ticker: p for p in price_service.prices(tickers, self.fiat[0])}
        for balance in self.balance.values():
            if balance.ticker not in prices:
                balance.value = 0
                balance.amount = 0
                continue
            balance.update_value(prices[balance.ticker])
            if balance.value < MIN_VAL:
                balance.amount = 0

    def to_dict(self):
        result = {}
        for b in self.balance.values():
            if b.value > 0:
                result[b.ticker] = {
                    "amount": b.amount_float,
                    self.fiat[0]: b.value
                }
        return result


    @staticmethod
    def wallet_name(wallet_id: int):
        return WALLETS[wallet_id]

    @property
    def type_name(self):
        return WALLETS[self.id]
