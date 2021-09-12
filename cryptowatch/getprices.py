import json
from typing import List

import requests

BINANCE_URL = "https://www.binance.com/api/v3/ticker/price"
SPECIAL_CASES = ["BETHEUR", "AUDIOEUR", "MBOXEUR", "EUREUR", "MLNEUR", "IDEXEUR", "SYSEUR", "THETAEUR", "SKLEUR"]


class Price:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

    def __str__(self):
        return f"{self.symbol}\t{self.price:,.8f}".replace(".", "%").replace(",", ".").replace("%", ",")


def get_price(ticker: str) -> Price:
    try:
        response = requests.request(method="GET", url=BINANCE_URL, params={"symbol": ticker})
        resp_json = response.json()
        return Price(resp_json["symbol"], float(resp_json["price"]))
    except:
        return None


def convert_two_steps(symbol: str, ticker1: str, ticker2: str):
    p1 = get_price(ticker1)
    p2 = get_price(ticker2)
    return Price(symbol, p1.price * p2.price)


def convert_two_steps2(symbol: str, ticker1: str, ticker2: str):
    p1 = get_price(ticker1)
    p2 = get_price(ticker2)
    return Price(symbol, p1.price * (1 /p2.price))


def two_steps_usdt(symbol: str):
    return convert_two_steps2(symbol + "EUR", symbol + "USDT", "EURUSDT")


def two_steps_btc(symbol: str):
    return convert_two_steps(symbol + "EUR", symbol + "BTC", "BTCEUR")


def betheur():
    return convert_two_steps("BETHEUR", "BETHETH", "ETHEUR")


def audioeur():
    return two_steps_usdt("AUDIO")


def mboxeur():
    return two_steps_usdt("MBOX")


def mlneur():
    return two_steps_usdt("MLN")


def idexeur():
    return two_steps_btc("IDEX")


def syseur():
    return two_steps_btc("SYS")


def thetaeur():
    return two_steps_btc("THETA")


def skleur():
    return two_steps_usdt("SKL")


def get_prices(tickers: List[str]):
    prices = []
    for ticker in tickers:
        if ticker in SPECIAL_CASES:
            prices.append(globals()[ticker.lower()]())
            continue
        price = get_price(ticker)
        if price:
            prices.append(price)
        else:
            print(f"Failed to fetch {ticker} price")
    return prices


def main():
    with open("config.json") as f:
        conf = json.load(f)
        for p in get_prices(conf["symbols"]):
            print(p)


if __name__ == '__main__':
    main()

