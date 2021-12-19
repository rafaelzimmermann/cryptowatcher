from typing import List

import math

from price.config import Config
from price.getprices import get_prices
from price.getprices import Price


class Balance:

    def __init__(self, ticker: str, amount: int = 0, fiat: List = ["EUR"]):
        self.ticker = ticker
        self.amount = amount
        self.fiat = {x: 0 for x in fiat}
        self.value = 0

    def update_value(self, price: Price):
        # TODO drop support multiple currencies
        self.value = price.price * self.amount_float

    @property
    def amount_float(self):
        return self.amount / math.pow(10, 8)

