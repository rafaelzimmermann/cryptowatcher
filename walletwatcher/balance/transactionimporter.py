#!/usr/local/bin/python

from typing import List

from parser.exodus import ExodusParser
from parser.parser import Parser

from storage.transactionstorage import TransactionStorage
from balance.balancecalculator import BalanceCalculator, Balance
from parser.binance import BinanceParser
from parser.cryptocom import CryptoComParser
from parser.daedalus import DaedalusParser

PARSERS = {
    "binance": BinanceParser,
    "cryptocom": CryptoComParser,
    "daedalus": DaedalusParser,
    "exodus": ExodusParser
}


class TransactionImporter:

    def __init__(self, storage: TransactionStorage) -> None:
        self.storage = storage

    def import_csv(self, file_path: str, source: str):
        parser = PARSERS[source](file_path)
        self._save([parser])


    def _save(self, parsers: List[Parser]):
        for parser in parsers:
            self.storage.save(parser.transactions())
