import math
from abc import ABC

from pathlib import Path
from typing import List

from model.transaction import Transaction, DEPOSIT, EXCHANGE, WITHDRAWAL
from model.wallet import WALLET_BINANCE
from model.wallet import WALLETS_PRECISION
from parser.parser import Parser
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class BinanceParser(Parser, ABC):
    """
        For now done in memory
    """

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.txids = {}
        self._transactions = self._load_transcations(dir_path)

    @staticmethod
    def _parse_amount(value) -> int:
        return int(float(value) * math.pow(10, WALLETS_PRECISION[WALLET_BINANCE])) if len(value) else 0

    @staticmethod
    def _parse_date(parts):
        return datetime.strptime(parts[1], DATE_FORMAT)

    @staticmethod
    def _parse_simple(line: str) -> Transaction:
        parts = line.split(',')
        date = BinanceParser._parse_date(parts)
        amount = BinanceParser._parse_amount(parts[5])
        if "fee" in parts[3].lower():
            t = Transaction(
                date=date,
                transaction_type=EXCHANGE,
                wallet=WALLET_BINANCE,
                fee_amount=amount,
                fee_currency=parts[4])
            return t.create_txid()

        if amount > 0:
            t = Transaction(
                date=date,
                transaction_type=DEPOSIT,
                wallet=WALLET_BINANCE,
                in_amount=amount,
                in_currency=parts[4])
            return t.create_txid()

        t = Transaction(
            date=date,
            transaction_type=WITHDRAWAL,
            wallet=WALLET_BINANCE,
            out_amount=amount,
            out_currency=parts[4])
        return t.create_txid()

    @staticmethod
    def _adjust_line(line):
        line = line.strip()
        if len(line) == 0:
            return None
        parts = line.split(",")
        if len(parts) == 6:
            line = '0,' + line
        return line

    def _load_transactions_from_file(self, csv_file) -> List[Transaction]:
        transactions = []
        skip_header = True
        with open(csv_file, 'r') as _file:
            for line in _file:
                if skip_header:
                    skip_header = False
                    continue
                line = BinanceParser._adjust_line(line)
                transaction = BinanceParser._parse_simple(line)
                if transaction.txid in self.txids:
                    continue
                transactions.append(transaction)
        return transactions

    def _load_transcations(self, dir_path: str) -> List:
        pathlist = Path(dir_path).glob('*.csv')
        transactions = []
        for path in pathlist:
            file_transactions = self._load_transactions_from_file(path)
            for t in file_transactions:
                self.txids[t.txid] = t
            transactions += file_transactions
        transactions.sort(key=lambda x: x.date)
        return transactions

    def transactions(self):
        return self._transactions
