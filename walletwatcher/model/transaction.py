import json
import math
import hashlib
from datetime import datetime

from model.wallet import WALLETS_PRECISION

DEPOSIT = "deposit"
INTEREST = "interest"
EXCHANGE = "exchange"
WITHDRAWAL = "withdrawal"

TRANSACTION_TYPE = ["undefined", DEPOSIT, EXCHANGE, WITHDRAWAL, INTEREST]


def transaction_type_int(type_str: str) -> int:
    return TRANSACTION_TYPE.index(type_str.lower())


def transaction_type_str(type_int: int) -> str:
    return TRANSACTION_TYPE[type_int]


class Transaction:
    # Sun Aug 08 2021 17:18:55 GMT+0200

    def __init__(self, id: int = 0, date: datetime = None, transaction_type: str = None, wallet: int = 0,
                 out_amount: int = 0, out_currency: str = None, fee_amount: int = 0, fee_currency: str = None,
                 in_amount: int = 0, in_currency: str = None, txid: str = None):
        self.id = id
        self._date = date
        self.type = transaction_type
        self.wallet = wallet
        self.out_amount = out_amount
        self.out_currency = out_currency
        self.fee_amount = fee_amount
        self.fee_currency = fee_currency
        self.in_amount = in_amount
        self.in_currency = in_currency
        self.txid = txid

    def to_dict(self):
        result = {
          "id": self.id,
          "date": self.date,
          "type": self.type,
          "wallet": self.wallet,
          "out_amount": self.out_amount,
          "out_amount_float": self.out_amount_float,
          "out_currency": self.out_currency,
          "fee_amount": self.fee_amount,
          "fee_amount_float": self.fee_amount_float,
          "fee_currency": self.fee_currency,
          "in_amount": self.in_amount,
          "in_amount_float": self.in_amount_float,
          "in_currency": self.in_currency,
          "txid": self.txid
        }
        delete_keys = [key for key in result if not result[key]]
        for key in delete_keys:
            del result[key]
        return result

    def create_txid(self):
        m = hashlib.sha1()
        m.update(str(self).encode("UTF8"))
        self.txid = m.hexdigest()
        return self

    @property
    def date(self) -> str:
        return self._date.isoformat()

    @property
    def out_amount_float(self) -> float:
        return self.out_amount / float(math.pow(10, WALLETS_PRECISION[self.wallet]))

    @property
    def in_amount_float(self) -> float:
        return self.in_amount / float(math.pow(10, WALLETS_PRECISION[self.wallet]))

    @property
    def fee_amount_float(self) -> float:
        return self.fee_amount / float(math.pow(10, WALLETS_PRECISION[self.wallet]))

    @property
    def currencies(self):
        return {x for x in [self.in_currency, self.fee_currency, self.out_currency]}

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        return Transaction(
            id=self.id if self.id else other.id,
            date=self._date if self._date else other._date,
            transaction_type=self.type if self.type else other.type,
            wallet=self.wallet if self.wallet else other.wallet,
            out_amount=self.out_amount if self.out_amount else other.out_amount,
            out_currency=self.out_currency if self.out_currency else other.out_currency,
            fee_amount=self.fee_amount if self.fee_amount else other.fee_amount,
            fee_currency=self.fee_currency if self.fee_currency else other.fee_currency,
            in_amount=self.in_amount if self.in_amount else other.in_amount,
            in_currency=self.in_currency if self.in_currency else other.in_currency,
            txid=self.txid if self.txid else other.txid
        )