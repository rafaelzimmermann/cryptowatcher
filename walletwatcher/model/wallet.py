from typing import List

from model.balance import Balance
from price.getprices import get_prices

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

MIN_VAL = 10


class Wallet:

    def __init__(self, id: int, name: str, type: int, fiat: List[str] = ["EUR"]):
        self.id = id
        self.name = name
        self.type = type
        self.fiat = fiat
        self.balance = {}

    def deposit(self, ticker: str, amount: int):
        if ticker not in self.balance:
            self.balance[ticker] = Balance(ticker, amount, self.fiat)
        self.balance[ticker].amount += amount

    def adjust_balance(self):
        for balance in self.balance.values():
            if balance.amount_float < MIN_VAL:
                balance.amount = 0

    def to_dict(self):
        result = {}
        for b in self.balance.values():
            result[b.ticker] = {
                "amount": b.amount_float
            }

        prices = get_prices([b.ticker for b in self.balance.values()], self.fiat[0])
        for price in prices:
            if price:
                result[price.ticker][self.fiat[0]] = price.price * result[price.ticker]["amount"]
        return result


    @staticmethod
    def wallet_name(wallet_id: int):
        return WALLETS[wallet_id]

    @property
    def type_name(self):
        return WALLETS[self.id]
