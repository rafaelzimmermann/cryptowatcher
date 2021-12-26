import math


class Balance:

    def __init__(self, ticker: str, amount: int = 0):
        self.ticker = ticker
        self.amount = amount

    @property
    def amount_float(self):
        return self.amount / math.pow(10, 8)

