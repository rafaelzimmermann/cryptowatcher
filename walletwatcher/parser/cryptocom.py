import math
from abc import ABC

from pathlib import Path
from typing import List

from model.transaction import Transaction, EXCHANGE, WITHDRAWAL
from model.wallet import WALLET_CRYPTOCOM
from model.wallet import WALLETS_PRECISION
from parser.parser import Parser
from datetime import datetime

from model.transaction import DEPOSIT

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class CryptoComParser(Parser, ABC):
    """
        For now done in memory
    """

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self._txids = set([])
        self._transactions = self._load_transactions(dir_path)

    @staticmethod
    def _parse_amount(value) -> int:
        return int(float(value) * math.pow(10, WALLETS_PRECISION[WALLET_CRYPTOCOM])) if len(value) else 0

    @staticmethod
    def _get_transaction_type(value: str) -> str:
        if any(t in value for t in [WITHDRAWAL, 'card_cashback_reverted', 'dust_conversion_debited']):
            return WITHDRAWAL
        if any(t in value for t in ['purchase', 'crypto_exchange', 'recurring_buy_order']):
            return EXCHANGE
        if any(t in value for t in ['referral_card_cashback', 'mco_stake_reward', 'reimbursement', 'dust_conversion_credited']):
            return DEPOSIT
        return None
    
    @staticmethod
    def _parse_line(line: str) -> Transaction:
        parts = line.split(',')
        # 0 - Timestamp (UTC)
        # 1 - Transaction Description
        # 2 - Currency
        # 3 - Amount
        # 4 - To Currency
        # 5 - To Amount
        # 6 - Native Currency
        # 7 - Native Amount
        # 8 - Native Amount (in USD)
        # 9 - Transaction Kind
        t_type = CryptoComParser._get_transaction_type(parts[9])
        if not t_type:
            return None
        t = Transaction(
            id=0,
            date=datetime.strptime(parts[0], DATE_FORMAT) if parts[0] else None,
            transaction_type=t_type,
            wallet=WALLET_CRYPTOCOM,
            out_amount=CryptoComParser._parse_amount(parts[3]),
            out_currency=parts[2],
            in_amount=CryptoComParser._parse_amount(parts[5]),
            in_currency=parts[4]
        )
        return t.create_txid()

    @staticmethod
    def _load_transactions_from_file(csv_file) -> List[Transaction]:
        transactions = []
        skip_header = True
        with open(csv_file, 'r') as _file:
            for line in _file:
                if skip_header:
                    skip_header = False
                    continue
                transaction = CryptoComParser._parse_line(line)
                if not transaction:
                    continue
                if not transaction.txid:
                    print("MISSING TXID:", transaction)
                transactions.append(transaction)
        return transactions

    def _load_transactions(self, dir_path: str) -> List:
        pathlist = Path(dir_path).glob('*.csv')
        transactions = []
        for path in pathlist:
            for t in CryptoComParser._load_transactions_from_file(path):
                if t.txid not in self._txids:
                    transactions.append(t)
                    self._txids.add(t.txid)

        return transactions

    def transactions(self):
        return self._transactions
