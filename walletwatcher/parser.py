import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from transaction import Transaction, DATE_FORMAT
from wallet import WALLET_EXODUS
from datetime import datetime

from wallet import WALLETS_PRECISION


class Parser(ABC):

    @abstractmethod
    def transactions(self):
        pass


class ExodusParser(Parser, ABC):
    """
        For now done in memory
    """

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self._transactions = ExodusParser._load_transcations(dir_path)

    @staticmethod
    def _parse_amount(value) -> int:
        return int(float(value) * math.pow(10, WALLETS_PRECISION[WALLET_EXODUS])) if len(value) else 0

    @staticmethod
    def _parse_line(line: str) -> Transaction:
        parts = line.split(',')
        # DATE,TYPE,FROMPORTFOLIO,TOPORTFOLIO,OUTAMOUNT,OUTCURRENCY,FEEAMOUNT,FEECURRENCY,TOADDRESS,OUTTXID,OUTTXURL,
        # INAMOUNT,INCURRENCY,INTXID,INTXURL,ORDERID,PERSONALNOTE
        return Transaction(
            id=0,
            date=datetime.utcfromtimestamp(datetime.strptime(parts[0][:33], DATE_FORMAT).timestamp()) if parts[0] else None,
            transaction_type=parts[1],
            wallet=WALLET_EXODUS,
            out_amount=ExodusParser._parse_amount(parts[4]),
            out_currency=parts[5],
            fee_amount=ExodusParser._parse_amount(parts[6]),
            fee_currency=parts[7],
            in_amount=ExodusParser._parse_amount(parts[11]),
            in_currency=parts[12],
            txid=parts[13] if parts[13] else parts[9]
        )

    @staticmethod
    def _load_transactions_from_file(csv_file) -> List[Transaction]:
        transactions = []
        skip_header = True
        with open(csv_file, 'r') as _file:
            for line in _file:
                if skip_header:
                    skip_header = False
                    continue
                transaction = ExodusParser._parse_line(line)
                if not transaction.txid:
                    print("MISSING TXID:", transaction)
                transactions.append(transaction)
        return transactions

    @staticmethod
    def _load_transcations(dir_path: str) -> dict:
        pathlist = Path(dir_path).glob('*.csv')
        transactions = []
        for path in pathlist:
            transactions += ExodusParser._load_transactions_from_file(path)
        return transactions

    def transactions(self):
        return self._transactions
