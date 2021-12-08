#!/usr/local/bin/python

from typing import List
from parser.parser import Parser

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator, Balance
from parser.binance import BinanceParser
from parser.cryptocom import CryptoComParser
from parser.daedalus import DaedalusParser

PARSERS = {
    "binance": BinanceParser,
    "cryptocom": CryptoComParser,
    "daedalus": DaedalusParser
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


def calc_balance(parser: Parser):
    balance = Balance()
    for t in parser.transactions():
        balance.add_transaction(t)
    balance.adjust_balance()
    print(balance)


if __name__ == '__main__':
    # exec_import(parsers=[ExodusParser('/wallets_data/exodus')])
    calc_balance(DaedalusParser('/Users/rzimmermann/personal_workspace/cryptowatch/wallets_data/daedalus'))
