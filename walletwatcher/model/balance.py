from typing import List

import math

from price.config import Config
from price.getprices import get_prices


class Balance:

    def __init__(self, ticker: str, amount: int = 0, fiat: List = ["EUR"]):
        self.ticker = ticker
        self.amount = amount
        self.fiat = {x: 0 for x in fiat}

    def update_fiat(self, config: Config):
        for f in self.fiat:
            get_prices(self.fiat.keys(), f, config)

    @property
    def amount_float(self):
        return self.amount / math.pow(10, 8)

