from model.balance import Balance
from storage.transactionstorage import TransactionStorage


class BalanceCalculator:

    def __init__(self, storage: TransactionStorage):
        self.storage = storage

    def calculate_from_beginning(self) -> Balance:
        balance = Balance()
        for t in self.storage.all_transactions():
            balance.add_transaction(t)
        balance.adjust_balance()
        return balance
