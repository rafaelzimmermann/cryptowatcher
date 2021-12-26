import time 


class Price:
    def __init__(self, ticker: str, fiat: str, symbol: str, price: float, source="binance", time: float = time.time()):
        self.ticker = ticker
        self.fiat = fiat
        self.symbol = symbol
        self.price = price
        self.source = source
        self.time = time

    def to_csv(self):
        return f"{self.ticker},{self.fiat},{self.symbol},{self.price},{self.source},{time.time()}"

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "price": self.price,
            "currency": self.fiat
        }

    @staticmethod
    def from_csv(line):
        parts = line.split(',')
        return Price(ticker=parts[0], fiat=parts[1], symbol=parts[2], price=float(parts[3]), source=parts[4], time=float(parts[5]))

    def __str__(self):
        return f"{self.symbol}\t{self.price:,.8f}".replace(".", "%").replace(",", ".").replace("%", ",")