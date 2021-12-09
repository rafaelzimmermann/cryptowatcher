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


def import_csv(file_path: str, source: str):
    parser = PARSERS[source](file_path)
    exec_import([parser])


def exec_import(parsers: List[Parser]):
    storage = TransactionStorage()
    for parser in parsers:
        storage.save(parser.transactions())
    balance_calculator = BalanceCalculator(storage)
    balance_calculator.calculate_from_beginning()
