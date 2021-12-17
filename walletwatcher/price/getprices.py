import json
import time
from typing import List, Optional
import concurrent.futures

import requests
from requests import Session

from price.config import Config

BINANCE_URL = "https://www.binance.com/api/v3/ticker/price"
BINANCE_EXCHANGE_INFO = "https://api.binance.com/api/v3/exchangeInfo"
COIN_MARKET_CAP_QUOTE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


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

    @staticmethod
    def from_csv(line):
        parts = line.split(',')
        return Price(ticker=parts[0], fiat=parts[1], symbol=parts[2], price=float(parts[3]), source=parts[4], time=float(parts[5]))

    def __str__(self):
        return f"{self.symbol}\t{self.price:,.8f}".replace(".", "%").replace(",", ".").replace("%", ",")


def get_binance_price(ticker: str, currency: str) -> Optional[Price]:
    try:
        symbol = f"{ticker}{currency}"
        response = requests.request(method="GET", url=BINANCE_URL, params={"symbol": symbol})
        resp_json = response.json()
        p = Price(ticker=ticker, fiat=currency, symbol=resp_json["symbol"], price=float(resp_json["price"]))
        save_price(p)
        return p
    except:
        return load_price(ticker, currency)


def load_price(ticker: str, fiat: str) -> Price:
    try:
        with open(f'cache/price_cache_{ticker}_{fiat}', 'r') as _f:
            return Price.from_csv(_f.read())
    except:
        None


def save_price(price: Price):
    try:
        with open(f'cache/price_cache_{price.ticker}_{price.fiat}', 'w') as _f:
            _f.write(price.to_csv())
    except Exception as e:
        print(e)


def eleapsed_time_minutes(start, end):
    return (end - start) / 60


def get_price_coinmarketcap(ticker: str, currency: str, api_key: str, rate_min: int) -> Optional[Price]:
    old_price = load_price(ticker, currency)
    if old_price and eleapsed_time_minutes(old_price.time, time.time()) < rate_min:
        return old_price

    parameters = {
        'symbol': ticker,
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(COIN_MARKET_CAP_QUOTE_URL, params=parameters)
        data = json.loads(response.text)
        price = data["data"][ticker]["quote"][currency]["price"]
        p = Price(ticker=ticker, fiat=currency, symbol=f"{ticker}{currency}", price=price, source="coinmarketcap")
        save_price(p)
        return p
    except Exception as e:
        return old_price


def resolve_price(available_symbols: List[str], ticker: str, currency: str) -> Optional[Price]:
    if f"{ticker}{currency}" in available_symbols:
        return get_binance_price(ticker, currency)
    for symbol in available_symbols:
        if symbol.endswith(currency):
            bridge_ticker = symbol.replace(currency, "")
            bridge_symbol = f"{ticker}{bridge_ticker}"
            if bridge_symbol in available_symbols:
                p1 = get_binance_price(ticker, bridge_ticker)
                p2 = get_binance_price(symbol.replace(currency, ''), currency)
                return Price(ticker=ticker, fiat=currency, symbol=f"{ticker}{currency}", price=p1.price * p2.price)
    return None


def get_available_symbols() -> list:
    response = requests.request(method="GET", url=BINANCE_EXCHANGE_INFO)
    resp_json = response.json()
    return [item["symbol"] for item in resp_json["symbols"]]

def get_price(ticker, currency, available_symbols, config) -> Price:
    symbol = ticker + currency
    price = None
    if symbol in available_symbols:
        price = get_binance_price(ticker, currency)
    else:
        price = resolve_price(available_symbols, ticker, currency)
    if not price and config and config.coin_market_cap:
        price = get_price_coinmarketcap(ticker, currency, config.coin_market_cap["apiKey"], 10)
    return price


def get_prices(tickers: List[str], currency: str, config: Config = None):
    available_symbols = get_available_symbols()
    prices = []
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        for ticker in tickers:
            symbol = ticker + currency
            futures.append(executor.submit(get_price, ticker, currency, available_symbols, config))
        for future in concurrent.futures.as_completed(futures):
            try:
                price = future.result()
                if price:
                    prices.append(price)
            except Exception as e:
                print(e)        
    return prices


def main():
    conf = Config("config.json")
    for currency in conf.currencies:
        print(currency)
        for p in get_prices(conf.tickers, currency, conf):
            print(p)
        print("--------")


if __name__ == '__main__':
    main()
