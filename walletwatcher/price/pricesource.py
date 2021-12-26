import json
import requests

from requests import Session

from model.price import Price
import price.binance as binance


class PriceSource:

    def __init__(self) -> None:
        pass

    def get_current_price(self, ticker: str, fiat:str):
        raise NotImplementedError()

    def get_intraday_price(self, ticker: str, fiat: str):
        raise NotImplementedError()

BINANCE_URL = 'https://www.binance.com/api/v3/ticker/price'


class BinancePriceSource(PriceSource):

    def __init__(self) -> None:
        pass

    def _fetch_price(self, ticker: str, fiat: str):
        symbol = f"{ticker}{fiat}"
        response = requests.request(method="GET", url=BINANCE_URL, params={"symbol": symbol})
        resp_json = response.json()
        return Price(ticker=ticker, fiat=fiat, symbol=resp_json["symbol"], price=float(resp_json["price"]))
    
    
    def get_current_price(self, ticker: str, fiat: str):
        if f"{ticker}{fiat}" in binance.AVAILABLE_SYMBOLS:
            return self._fetch_price(ticker, fiat)
        if f"{fiat}{ticker}" in binance.AVAILABLE_SYMBOLS:
            p = self._fetch_price(fiat, ticker)
            return Price(ticker=ticker, currency=fiat, symbol=f"{fiat}{ticker}", price=1/p.price)


COIN_MARKET_CAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


class CoinMarketCap(PriceSource):

    def __init__(self, apikey: str) -> None:
        self.apikey = apikey

    def get_current_price(self, ticker: str, fiat: str):
        if not self.apikey:
            return None
        parameters = {
            'symbol': ticker,
            'convert': fiat
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.apikey,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(COIN_MARKET_CAP_URL, params=parameters)
        data = json.loads(response.text)
        price = data["data"][ticker]["quote"][fiat]["price"]
        p = Price(ticker=ticker, fiat=fiat, symbol=f"{ticker}{fiat}", price=price, source="coinmarketcap")
        return p
        

ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'

class AlphaVantage(PriceSource):

    def __init__(self, apikey: str) -> None:
        self.apikey = apikey

    def get_current_price(self, ticker: str, fiat: str):
        raise NotImplementedError()

    def get_intraday_price(self, ticker: str, fiat: str):
        url = ALPHA_VANTAGE_URL + '?function=DIGITAL_CURRENCY_DAILY&symbol=' + ticker + '&market=' + fiat + '&apikey=' + self.apikey
        r = requests.get(url)
        data = r.json()

    


    