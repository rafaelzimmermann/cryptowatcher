from typing import List

import math

from price.config import Config
from price.getprices import get_prices
from price.getprices import Price


class Balance:

    def __init__(self, ticker: str, amount: int = 0):
        self.ticker = ticker
        self.amount = amount

    @property
    def amount_float(self):
        return self.amount / math.pow(10, 8)

