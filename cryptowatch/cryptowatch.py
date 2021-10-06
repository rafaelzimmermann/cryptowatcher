#!/usr/local/bin/python

import json
import os

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler

from getprices import get_prices, Price

registry = CollectorRegistry()
gprice = Gauge('crypto_price', 'Price', labelnames=['symbol'], registry=registry)
gbalance = Gauge('crypto_balance', 'Balance', labelnames=['symbol'], registry=registry)


def my_auth_handler(url, method, timeout, headers, data):
    username = 'admin'
    password = 'admin'
    return basic_auth_handler(url, method, timeout, headers, data, username, password)


def push_price(price: Price):
    gprice.labels(symbol=price.symbol).set(price.price)


def push_balance(symbol: str, value: float):
    gbalance.labels(symbol=symbol).set(value)


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + "/config.json") as f:
        conf = json.load(f)
        for p in get_prices(conf["watchPrices"], conf["currency"]):
            push_price(p)

    for key in sorted(conf["wallet"].keys()):
        price = get_prices([key], conf["currency"])[0]
        value = price.price * conf["wallet"][key] if price else 0.0
        push_balance(key, value)

    push_to_gateway('pushgateway:9091', job='pushBalance', registry=registry, handler=my_auth_handler)


if __name__ == '__main__':
    main()
