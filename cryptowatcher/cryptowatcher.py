#!/usr/local/bin/python

import os

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler

from config import Config
from getprices import get_prices, Price

registry = CollectorRegistry()
gprice = Gauge('crypto_price', 'Price', labelnames=['symbol', 'ticker', 'fiat'], registry=registry)
gbalance = Gauge('crypto_balance', 'Balance', labelnames=['symbol', 'ticker', 'fiat'], registry=registry)


def my_auth_handler(url, method, timeout, headers, data):
    username = 'admin'
    password = 'admin'
    return basic_auth_handler(url, method, timeout, headers, data, username, password)


def push_price(price: Price):
    gprice.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat).set(price.price)


def push_balance(price: Price, balance: float):
    gbalance.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat).set(balance)


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    conf = Config(path + "/config.json")

    for currency in conf.currencies:
        for price in get_prices(conf.tickers, currency):
            push_price(price)

        for price in get_prices(sorted(conf.wallet.keys()), currency):
            balance = price.price * conf.wallet[price.ticker] if price else 0.0
            push_balance(price, balance)

    push_to_gateway('pushgateway:9091', job='pushBalance', registry=registry, handler=my_auth_handler)


if __name__ == '__main__':
    main()
