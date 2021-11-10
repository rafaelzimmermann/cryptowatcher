#!/usr/local/bin/python

from typing import List
from parser.parser import Parser

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator, Balance
from parser.binance import BinanceParser


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
    calc_balance(BinanceParser('/Users/rzimmermann/personal_workspace/cryptowatch/wallets_data/binance'))