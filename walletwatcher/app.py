import json
import os

from flask import Flask, jsonify, request, make_response
from logging.config import dictConfig


from storage.transactionstorage import TransactionStorage
from balance.balancecalculator import BalanceCalculator
from balance.transactionimporter import TransactionImporter
from price.watcher import PriceWatcher
from price.priceservice import PriceService
from price.config import Config
from storage.ConfigStorage import ConfigStorage
from storage.Database import Database
from storage.portifoliostorage import PortifolioStorage
from werkzeug.utils import secure_filename


BAD_REQUEST = 400
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = '/tmp'

config = Config('config.json')
if config.logging:
    dictConfig(config.logging)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

database = Database()
transaction_storage = TransactionStorage(database=database)
portfolio_storage = PortifolioStorage(database=database)
config_storage = ConfigStorage(database=database)
price_service = PriceService(config, app.logger)
price_watcher = PriceWatcher(price_service=price_service, conf=config, logger=app.logger)


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


@app.route("/v1/price/<ticker>/<currency>")
def get_price(ticker, currency):
    return jsonify(price_service.prices(tickers=[ticker], currency=currency))


@app.route("/v1/prices")
def get_prices():
    tickers = request.args.get('tickers').split(',')
    currency = request.args.get('currency')
    return jsonify([p.to_dict() for p in price_service.prices(tickers, currency)])

# TODO rename to portfolio
@app.route("/v1/balance")
def get_balance():
    portfolio = portfolio_storage.get()
    if portfolio:
        response = make_response(portfolio,200)
        response.headers["Content-Type"] = "application/json"
        return response
    bc = BalanceCalculator(transaction_storage)
    portfolio = bc.calculate_from_beginning()

    response = jsonify(portfolio.to_dict())
    portfolio_storage.save(response.data)
    return response

@app.route("/v1/transactions")
def get_transactions():
    bc = BalanceCalculator(transaction_storage)
    limit = get_int_param('limit', DEFAULT_LIMIT)
    offset = get_int_param('offset', DEFAULT_OFFSET)
    result = [t.to_dict() for t in bc.get_transactions(limit=limit, offset=offset)]
    return jsonify(result)


@app.route("/v1/wallet/<source>", methods=["POST"])
def import_wallet_csv(source):
    if 'file' not in request.files:
        return jsonify({"error": "Missing file"}), BAD_REQUEST
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Missing file name"}), BAD_REQUEST
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        TransactionImporter(storage=transaction_storage).import_csv(app.config['UPLOAD_FOLDER'], source)
        return jsonify({}), 200

@app.route("/v1/config", methods=["POST"])
def update_config():
    currency = request.form.currency
    balance_config = request.form
    config = Config(currency=currency, balance_config=balance_config)
    config_storage.update(config)
    return jsonify({}), 200

    

@app.route('/metrics')
def track_prices():
    return price_watcher.watch_price_metrics()
    
