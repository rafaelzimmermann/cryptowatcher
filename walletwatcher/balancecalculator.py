import json
import math

from transactionstorage import TransactionStorage
from transaction import Transaction
from wallet import Wallet, WALLETS_PRECISION

MIN_VAL = 10


class Balance:

    def __init__(self):
        self.balance = {}

    def add_transaction(self, transaction: Transaction):
        wallet_name = Wallet.wallet_name(transaction.wallet)
        if wallet_name not in self.balance:
            self.balance[wallet_name] = {}
        wallet_balance = self.balance[wallet_name]

        if transaction.in_amount != 0:
            if transaction.in_currency not in wallet_balance:
                wallet_balance[transaction.in_currency] = 0
            wallet_balance[transaction.in_currency] += transaction.in_amount

        if transaction.out_amount != 0:
            if transaction.out_currency not in wallet_balance:
                wallet_balance[transaction.out_currency] = 0
            wallet_balance[transaction.out_currency] += transaction.out_amount

        if transaction.fee_amount != 0:
            if transaction.fee_currency not in wallet_balance:
                wallet_balance[transaction.fee_currency] = 0
            wallet_balance[transaction.fee_currency] += transaction.fee_amount

    def adjust_balance(self):
        for wallet_key in self.balance:
            wallet = self.balance[wallet_key]
            for key in wallet:
                if wallet[key] < MIN_VAL:
                    wallet[key] = 0

    def to_dict(self) -> dict:
        result = {}
        for wallet in self.balance:
            result[wallet] = {}
            for key in self.balance[wallet]:
                if self.balance[wallet][key] > 0:
                    result[wallet][key] = self.balance[wallet][key] / float(math.pow(10, WALLETS_PRECISION[1]))
        return result

    def __repr__(self):
        return json.dumps(self.to_dict())


class BalanceCalculator:

    def __init__(self, storage: TransactionStorage):
        self.storage = storage

    def calculate_from_beginning(self) -> Balance:
        balance = Balance()
        for t in self.storage.all_transactions():
            balance.add_transaction(t)
        balance.adjust_balance()
        return balance
