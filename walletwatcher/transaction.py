import json
import math
from datetime import datetime

from wallet import WALLETS_PRECISION

DATE_FORMAT = "%a %b %d %Y %H:%M:%S %Z%z"
TRANSACTION_TYPE = ["undefined", "deposit", "exchange", "withdrawal"]


def transaction_type_int(type_str: str) -> int:
    return TRANSACTION_TYPE.index(type_str.lower())


def transaction_type_str(type_int: int) -> str:
    return TRANSACTION_TYPE[type_int]


class Transaction:
    # Sun Aug 08 2021 17:18:55 GMT+0200

    def __init__(self, id: int, date: datetime, transaction_type: str, wallet: int, out_amount: int, out_currency: str,
                 fee_amount: int, fee_currency: str, in_amount: int, in_currency: str, txid: str):
        self.id = id if id else None
        self._date = date
        self.type = transaction_type
        self.wallet = wallet if wallet else 0
        self.out_amount = out_amount
        self.out_currency = out_currency if out_currency else ""
        self.fee_amount = fee_amount
        self.fee_currency = fee_currency if fee_currency else ""
        self.in_amount = in_amount
        self.in_currency = in_currency if in_currency else ""
        self.txid = txid if txid else ""

    def to_dict(self):
        return {
          "id": self.id,
          "date": self._date.isoformat(),
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