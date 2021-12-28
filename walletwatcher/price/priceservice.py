import concurrent.futures
from os import stat
from typing import List

from price.filecache import FileCache
from price.config import Config
from price.pricesource import BinancePriceSource, CoinMarketCap


BINANCE_TTL = 60
COIN_MARKET_CAP_TTL = 3600

class PriceService:

    def __init__(self, config: Config, logger):
        self.price_cache = FileCache(path='cache/')
        self.binance = BinancePriceSource()
        self.coinmarketcap = CoinMarketCap(apikey=config.coin_market_cap['apiKey'] if config.coin_market_cap else "")
        self.config = config
        self.logger = logger

    def _get_and_cache_prices(self, ticker: str, fiat: str):
        if not ticker:
            raise Exception("Invalid params")
        self.logger.info(f"Getting price from source: {ticker}")
        price = self.binance.get_current_price(ticker, fiat)
        if not price:
            price = self.coinmarketcap.get_current_price(ticker, fiat)         
        if not price:
            return None   
        if price.source == 'binance':
            ttl = BINANCE_TTL
        else:
            ttl = COIN_MARKET_CAP_TTL
        self.price_cache.set_item(f"{ticker}{fiat}", price, ttl)
        return price

    def prices(self, tickers: List[str], currency: str, skip_cache: bool = False):
        if skip_cache:
            return self._get_and_cache_prices(tickers, currency)
        
        cached = []
        not_cached = []
        for ticker in tickers:
            price = self.price_cache.get_item(f'{ticker}{currency}')
            if price:
                cached.append(price)
            else:
                not_cached.append(ticker)

        prices = []
        futures = []
        
        if not_cached:
            with concurrent.futures.ThreadPoolExecutor(max_workers = len(tickers)) as executor:
                for ticker in not_cached:
                    futures.append(executor.submit(self._get_and_cache_prices, ticker, currency))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        price = future.result()
                        if price:
                            prices.append(price)
                    except Exception as e:
                        print(e)        
        return cached + prices
    
        
def main():
    import logging
    conf = Config("config.json")
    ps = PriceService(conf, logging)
    
    for currency in conf.currencies:
        print(currency)
        prices = ps.prices(conf.tickers, currency)
        for ticker in conf.tickers:
            for p in prices:
                if ticker == p.ticker:
                    print(p)
                    break


if __name__ == '__main__':
    main()