import json
from typing import List

import requests

BINANCE_URL = "https://www.binance.com/api/v3/ticker/price"
BINANCE_EXCHANGE_INFO = "https://api.binance.com/api/v3/exchangeInfo"


class Price:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

    def __str__(self):
        return f"{self.symbol}\t{self.price:,.8f}".replace(".", "%").replace(",", ".").replace("%", ",")


def get_price(symbol: str) -> Price:
    try:
        response = requests.request(method="GET", url=BINANCE_URL, params={"symbol": symbol})
        resp_json = response.json()
        return Price(resp_json["symbol"], float(resp_json["price"]))
    except:
        return None


def resolve_price(available_symbols: List[str], ticker: str, currency: str) -> Price:
    for symbol in available_symbols:
        if symbol.endswith(currency):
            bridge_ticker = symbol.replace(currency, "")
            bridge_symbol = f"{ticker}{bridge_ticker}"
            if bridge_symbol in available_symbols:
                p1 = get_price(bridge_symbol)
                p2 = get_price(symbol)
                return Price(f"{ticker}{currency}", p1.price * p2.price)


def get_available_symbols() -> list:
    response = requests.request(method="GET", url=BINANCE_EXCHANGE_INFO)
    resp_json = response.json()
    return [item["symbol"] for item in resp_json["symbols"]]


def get_prices(tickers: List[str], currency: str):
    available_symbols = get_available_symbols()
    prices = []
    for ticker in tickers:
        symbol = ticker + currency
        if symbol in available_symbols:
            price = get_price(symbol)
        else:
            price = resolve_price(available_symbols, ticker, currency)

        if price:
            prices.append(price)
        else:
            print(f"Failed to fetch {ticker} price")
    return prices


def main():
    with open("config.json") as f:
        conf = json.load(f)
        for p in get_prices(conf["watchPrices"], conf["currency"]):
            print(p)


if __name__ == '__main__':
    main()

