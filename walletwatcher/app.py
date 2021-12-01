from flask import Flask, jsonify

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator

app = Flask(__name__)

transaction_storage = TransactionStorage()

@app.route("/v1/balance")
def get_balance():
    bc = BalanceCalculator(transaction_storage)
    balance = bc.calculate_from_beginning()
    return jsonify(balance.to_dict())

