from prometheus_client import Gauge, CollectorRegistry, generate_latest

from price.config import Config
from price.getprices import get_prices, Price


class PriceWatcher:

    def __init__(self, logger) -> None:
        self.registry = CollectorRegistry()
        self.gprice = Gauge('crypto_price', 'Price', labelnames=['symbol', 'ticker', 'fiat', 'source'], registry=self.registry)
        self.gbalance = Gauge('crypto_balance', 'Balance', labelnames=['symbol', 'ticker', 'fiat', 'source'], registry=self.registry)
        self.logger = logger

    def watch_price_metrics(self):
        conf = Config("/app/config.json")
        self.logger.info("Downloading prices")
        for currency in conf.currencies:
            for price in get_prices(conf.tickers, currency, conf):
                self.gprice.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat, source=price.source).set(price.price)

            for price in get_prices(sorted(conf.wallet.keys()), currency, conf):
                balance = price.price * conf.wallet[price.ticker] if price else 0.0
                self.gbalance.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat, source=price.source).set(balance)
        return generate_latest(self.registry)
