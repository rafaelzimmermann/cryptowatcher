import os

from flask import Flask, jsonify, request, redirect, url_for

from transactionstorage import TransactionStorage
from balancecalculator import BalanceCalculator
from balanceimporter import import_csv
from werkzeug.utils import secure_filename


BAD_REQUEST = 400

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

transaction_storage = TransactionStorage()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/v1/balance")
def get_balance():
    bc = BalanceCalculator(transaction_storage)
    balance = bc.calculate_from_beginning()
    return jsonify(balance.to_dict())


@app.route("/v1/wallet/<name>", methods=["POST"])
def import_wallet_csv(name):
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "Missing file"}), BAD_REQUEST
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "Missing file name"}), BAD_REQUEST
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        import_csv(app.config['UPLOAD_FOLDER'], name)
        return jsonify({}), 200
