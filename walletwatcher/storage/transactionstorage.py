import psycopg2

from typing import List, Optional
from model.transaction import Transaction

from model.transaction import transaction_type_int, transaction_type_str


def create_connection():
    return psycopg2.connect(
        database="walletwatcher",
        user="walletwatcher",
        password="walletwatcher",
        host="postgres",
        port="5432"
    )


def init_database(connection):
    sql_file = open('/app/database.sql', 'r')
    connection.autocommit = True
    connection.rollback()
    with connection, connection.cursor() as cursor:
        cursor.execute(sql_file.read())
    connection.autocommit = False


class TransactionStorage:

    def __init__(self):
        self.connection = create_connection()
        self.connection.autocommit = True
        self.connection.rollback()

    def _parse_row(self, row) -> Transaction:
        return Transaction(
                id=row[0],
                date=row[1],
                transaction_type=transaction_type_str(row[2]),
                wallet=row[3],
                out_amount=row[4],
                out_currency=row[5],
                fee_amount=row[6],
                fee_currency=row[7],
                in_amount=row[8],
                in_currency=row[9],
                txid=row[10])

    def get_by_txid(self, txid) -> Optional[Transaction]:
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, date, type, wallet, out_amount, out_currency, fee_amount, fee_currency, in_amount, in_currency, txid
        FROM transaction
        WHERE txid = %s
        ''', (txid,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._parse_row(row)

    def save(self, transactions: List[Transaction]):
        cursor = self.connection.cursor()
        for t in transactions:
            if self.get_by_txid(t.txid):
                continue
            try:
                cursor.execute('''
                INSERT INTO transaction 
                   (date, type, wallet, out_amount, out_currency, fee_amount, fee_currency, in_amount, in_currency, txid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (t.date, transaction_type_int(t.type), t.wallet, t.out_amount, t.out_currency, t.fee_amount,
                                t.fee_currency, t.in_amount, t.in_currency, t.txid,))

                self.connection.commit()
            except Exception as e:
                print('ERROR', t)
                print(e)

    def all_transactions(self) -> List[Transaction]:
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, date, type, wallet, out_amount, out_currency, fee_amount, fee_currency, in_amount, in_currency, txid
        FROM transaction
        ORDER by date;
        ''')
        transactions = []
        for row in cursor.fetchall():
            transactions.append(self._parse_row(row))
        return transactions

    def get_transactions(self, limit: int, offset: int) -> List[Transaction]:
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT id, date, type, wallet, out_amount, out_currency, fee_amount, fee_currency, in_amount, in_currency, txid
        FROM transaction
        ORDER by date
        LIMIT %s
        OFFSET %s
        ''', (limit, offset,))
        transactions = []
        for row in cursor.fetchall():
            transactions.append(self._parse_row(row))
        return transactions

