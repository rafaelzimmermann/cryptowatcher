#!/usr/local/bin/python

from typing import List
from parser import Parser
from parser import ExodusParser

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator, Balance


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


if __name__ == '__main__':
    exec_import(parsers=[ExodusParser('/wallets_data/exodus')])
