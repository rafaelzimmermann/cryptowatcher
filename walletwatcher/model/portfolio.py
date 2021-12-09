from typing import List

from model.transaction import Transaction
from model.wallet import Wallet


class Portfolio:

    def __init__(self):
        self.wallets = {}

    def add_transactions(self, transactions: List[Transaction]):
        for transaction in transactions:
            if transaction.wallet not in self.wallets:
                self.wallets[transaction.wallet] = \
                    Wallet(transaction.wallet, Wallet.wallet_name(transaction.wallet), transaction.type)
            wallet = self.wallets[transaction.wallet]

            if transaction.in_amount != 0:
                wallet.deposit(transaction.in_currency, transaction.in_amount)

            if transaction.out_amount != 0:
                wallet.deposit(transaction.out_currency, transaction.out_amount)

            if transaction.fee_amount != 0:
                wallet.deposit(transaction.fee_currency, transaction.fee_amount)
        for wallet in self.wallets.values():
            wallet.adjust_balance()

    def to_dict(self):
        wallets = self.wallets.values()
        return {wallet.name: wallet.to_dict() for wallet in wallets}



