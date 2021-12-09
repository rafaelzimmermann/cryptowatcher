import csv
import math
from abc import ABC

from pathlib import Path
from typing import List

from model.transaction import Transaction, DEPOSIT, WITHDRAWAL
from model.wallet import WALLET_DAEDALUS
from model.wallet import WALLETS_PRECISION
from parser.parser import Parser
from datetime import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


class DaedalusParser(Parser, ABC):
    """
        For now done in memory
    """

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self._txids = set([])
        self._transactions = self._load_transactions(dir_path)

    @staticmethod
    def _parse_amount(value) -> int:
        value = value.replace(',', '')
        return int(float(value) * math.pow(10, WALLETS_PRECISION[WALLET_DAEDALUS])) if len(value) else 0

    @staticmethod
    def _get_transaction_type(value: str) -> str:
        if 'received' in value.lower():
            return DEPOSIT
        if 'sent' in value.lower():
            return WITHDRAWAL
        raise Exception('Unknown type')

    @staticmethod
    def _parse_line(parts) -> Transaction:
        # 0 - ID
        # 1 - Type
        # 2 - TOTAL (ADA)
        # 3 - Sent amount (ADA)
        # 4 - Deposit amount (ADA)
        # 5 - Fee (ADA)
        # 6 - Tokens (unformatted amounts)
        # 7 - Date & time
        # 8 - Status
        # 9 - Addresses from
        # 10 - Addresses to
        # 11 - Withdrawals
        # TODO Handle token
        # TODO Add Fee info to transaction
        t = Transaction(
            id=0,
            date=datetime.strptime(parts[7], DATE_FORMAT) if parts[7] else None,
            transaction_type=DaedalusParser._get_transaction_type(parts[1]),
            wallet=WALLET_DAEDALUS,
            txid=parts[0]
        )

        amount = DaedalusParser._parse_amount(parts[2])
        if amount > 0:
            t += Transaction(
                in_amount=amount,
                in_currency="ADA"
            )
        else:
            t += Transaction(
                out_amount=amount,
                out_currency="ADA"
            )
        return t

    @staticmethod
    def _load_transactions_from_file(csv_file) -> List[Transaction]:
        transactions = []
        skip_header = True
        with open(csv_file, 'r') as _file:
            csvreader = csv.reader(_file, quotechar='"')
            for line in csvreader:
                if skip_header:
                    skip_header = False
                    continue
                transaction = DaedalusParser._parse_line(line)
                if not transaction.txid:
                    print("MISSING TXID:", transaction)
                transactions.append(transaction)
        return transactions

    def _load_transactions(self, dir_path: str) -> List:
        pathlist = Path(dir_path).glob('*.csv')
        transactions = []
        for path in pathlist:
            for t in DaedalusParser._load_transactions_from_file(path):
                if t.txid not in self._txids:
                    transactions.append(t)
                    self._txids.add(t.txid)
        return transactions

    def transactions(self):
        return self._transactions
