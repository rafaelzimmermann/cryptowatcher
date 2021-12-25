from typing import List

from model.balance import Balance

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

WALLETS_ID = {
    'Exodus': 1,
    'Binance': 2,
    'crypto.com': 3,
    'Daedalus': 4 
}

WALLETS_PRECISION = {
    1: 8,
    2: 8,
    3: 8,
    4: 8
}

MIN_VAL = 1


class Wallet:

    def __init__(self, id: int, name: str):
        # TODO drop mult fiat support
        self.id = id if id else WALLETS_ID[name]
        self.name = name if name else WALLETS[id]
        self.balance = {}

    def deposit(self, ticker: str, amount: int):
        if ticker not in self.balance:
            self.balance[ticker] = Balance(ticker, amount)
        self.balance[ticker].amount += amount

    def to_dict(self):
        result = {}
        for b in self.balance.values():
            if b.amount_float > 0:
                result[b.ticker] = {
                    "amount": b.amount_float
                }
        return result
    
    @staticmethod
    def from_dict(id: int, name: str, data: dict):
        wallet = Wallet(name)
        for ticker in data:
            wallet.deposit(ticker, data[ticker])

    @staticmethod
    def wallet_name(wallet_id: int):
        return WALLETS[wallet_id]

    @property
    def type_name(self):
        return WALLETS[self.id]
