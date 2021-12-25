import json
from typing import List

from model.transaction import Transaction
from model.wallet import Wallet
from price.priceservice import PriceService


class Portfolio:

    def __init__(self, price_service: PriceService = None):
        self.wallets = {}
        self.price_service = price_service

    def add_transactions(self, transactions: List[Transaction]):
        for transaction in transactions:
            if transaction.wallet not in self.wallets:
                self.wallets[transaction.wallet] = \
                    Wallet(transaction.wallet, Wallet.wallet_name(transaction.wallet))
            wallet = self.wallets[transaction.wallet]

            if transaction.in_amount != 0:
                wallet.deposit(transaction.in_currency, transaction.in_amount)

            if transaction.out_amount != 0:
                wallet.deposit(transaction.out_currency, transaction.out_amount)

            if transaction.fee_amount != 0:
                wallet.deposit(transaction.fee_currency, transaction.fee_amount)

    def to_dict(self):
        wallets = self.wallets.values()
        return {wallet.name: wallet.to_dict() for wallet in wallets}

    @staticmethod
    def from_json(payload: str):
        data = json.load(payload)
        portifolio = Portfolio()
        for wallet in data:
            portifolio.wallets[wallet] = Wallet.from_dict(data[wallet])
        return portifolio




