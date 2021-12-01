from flask import Flask

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator

app = Flask(__name__)

transaction_storage = TransactionStorage()

@app.route("/v1/balance")
def balance():
    bc = BalanceCalculator(transaction_storage)
    bc.calculate_from_beginning()
    return str(bc.balance)

