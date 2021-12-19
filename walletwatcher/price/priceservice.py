from typing import List
from cachetools import TTLCache

from price.getprices import get_prices
from price.config import Config

class PriceService:

    def __init__(self, config: Config):
        self.price_cache = TTLCache(ttl=600, maxsize=10000)
        self.config = config

    def _get_and_cache_prices(self, tickers: List[str], currency: str):
        result = get_prices(tickers, currency, self.config)
        for price in result:
            self.price_cache[price.ticker] = price
        return result

    def prices(self, tickers: List[str], currency: str, skip_cache: bool = False):
        if skip_cache:
            return self._get_and_cache_prices(tickers, currency)
        
        cached = []
        not_cached = []
        for ticker in tickers:
            try:
                cached.append(self.price_cache[ticker])
            except:
                not_cached.append(ticker)
        return cached + self._get_and_cache_prices(not_cached, currency)
    
        
        

    