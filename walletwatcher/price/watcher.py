from prometheus_client import Gauge, CollectorRegistry, generate_latest

from price.config import Config
from price.getprices import Price
from price.priceservice import PriceService


class PriceWatcher:

    def __init__(self, price_service: PriceService, conf: Config, logger) -> None:
        self.registry = CollectorRegistry()
        self.gprice = Gauge('crypto_price', 'Price', labelnames=['symbol', 'ticker', 'fiat', 'source'], registry=self.registry)
        self.gbalance = Gauge('crypto_balance', 'Balance', labelnames=['symbol', 'ticker', 'fiat', 'source'], registry=self.registry)
        self.logger = logger
        self.price_service = price_service
        self.config = conf

    def watch_price_metrics(self):
        self.logger.info("Downloading prices")
        for currency in self.config.currencies:
            for price in self.price_service.prices(self.config.tickers, currency, skip_cache=True):
                self.gprice.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat, source=price.source).set(price.price)

            for price in self.price_service.prices(sorted(self.config.wallet.keys()), currency):
                balance = price.price * self.config.wallet[price.ticker] if price else 0.0
                self.gbalance.labels(symbol=price.symbol, ticker=price.ticker, fiat=price.fiat, source=price.source).set(balance)
        return generate_latest(self.registry)
