import os

from flask import Flask, jsonify, request

from storage.transactionstorage import TransactionStorage
from balance.balancecalculator import BalanceCalculator
from balance.balanceimporter import import_csv
from price.watcher import PriceWatcher
from werkzeug.utils import secure_filename


BAD_REQUEST = 400
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
price_watcher = PriceWatcher(app.logger)
transaction_storage = TransactionStorage()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_int_param(name: str, default_val: int) -> int:
    try:
        value = int(request.args.get(name))
    except:
        return default_val
    if not value:
        return default_val
    return value


@app.route("/v1/balance")
def get_balance():
    bc = BalanceCalculator(transaction_storage)
    portfolio = bc.calculate_from_beginning()
    return jsonify(portfolio.to_dict())

@app.route("/v1/transactions")
def get_transactions():
    bc = BalanceCalculator(transaction_storage)
    limit = get_int_param('limit', DEFAULT_LIMIT)
    offset = get_int_param('offset', DEFAULT_OFFSET)

    result = [t.to_dict() for t in bc.get_transactions(limit=limit, offset=offset)]
    return jsonify(result)


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
    

@app.route('/metrics')
def track_prices():
    return price_watcher.watch_price_metrics()
    
