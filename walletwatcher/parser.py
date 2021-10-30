import json
from abc import ABC, abstractmethod
from datetime import datetime

from pathlib import Path


class Transaction:
    # Sun Aug 08 2021 17:18:55 GMT+0200
    DATE_FORMAT = "%a %b %d %Y %H:%M:%S %Z%z"

    def __init__(self, id, date, type, wallet, out_amount, out_currency, fee_amount,
                 fee_currency, in_amount, in_currency, txid):
        self.id = id if id else None
        self.date = datetime.utcfromtimestamp(datetime.strptime(date[:33], self.DATE_FORMAT).timestamp()) if date else None
        self.type = type if type else None
        self.wallet = wallet if wallet else None
        self.out_amount = out_amount if out_amount else None
        self.out_currency = out_currency if out_currency else None
        self.fee_amount = fee_amount if fee_amount else None
        self.fee_currency = fee_currency if fee_currency else None
        self.in_amount = in_amount if in_amount else None
        self.in_currency = in_currency if in_currency else None
        self.txid = txid if txid else None

    def to_dict(self):
        return {
          "id": self.id,
          "date": self.date.isoformat(),
          "type": self.type,
          "wallet": self.wallet,
          "out_amount": self.out_amount,
          "out_currency": self.out_currency,
          "fee_amount": self.fee_amount,
          "fee_currency": self.fee_currency,
          "in_amount": self.in_amount,
          "in_currency": self.in_currency,
          "txid": self.txid
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), )


class Parser(ABC):

    @abstractmethod
    def transactions(self):
        pass


class ExodusParser(Parser, ABC):
    """
        For now done in memory
    """

    WALLET = "Exodus"

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self._transactions = ExodusParser._load_transcations(dir_path).values()

    @staticmethod
    def _parse_line(line: str) -> Transaction:
        parts = line.split(',')
        # DATE,TYPE,FROMPORTFOLIO,TOPORTFOLIO,OUTAMOUNT,OUTCURRENCY,FEEAMOUNT,FEECURRENCY,TOADDRESS,OUTTXID,OUTTXURL,
        # INAMOUNT,INCURRENCY,INTXID,INTXURL,ORDERID,PERSONALNOTE
        return Transaction(
            id=None,
            date=parts[0],
            type=parts[1],
            wallet=ExodusParser.WALLET,
            out_amount=parts[4],
            out_currency=parts[5],
            fee_amount=parts[6],
            fee_currency=parts[7],
            in_amount=parts[11],
            in_currency=parts[12],
            txid=parts[13] if parts[13] else parts[9]
        )

    @staticmethod
    def _load_transactions_from_file(csv_file) -> dict:
        txid_transaction = {}
        skip_header = True
        with open(csv_file, 'r') as _file:
            for line in _file:
                if skip_header:
                    skip_header = False
                    continue
                transaction = ExodusParser._parse_line(line)
                if not transaction.txid:
                    print(transaction)
                txid_transaction[transaction.txid] = transaction
        return txid_transaction

    @staticmethod
    def _load_transcations(dir_path: str) -> dict:
        pathlist = Path(dir_path).glob('*.csv')
        txid_transaction = {}
        for path in pathlist:
            txid_transaction.update(ExodusParser._load_transactions_from_file(path))
        return txid_transaction

    def transactions(self):
        return self._transactions
