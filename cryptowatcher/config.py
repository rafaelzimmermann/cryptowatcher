import json


class Config:

    def __init__(self, config_json_path: str):
        with open(config_json_path) as f:
            conf = json.load(f)
            self.currencies = conf["currencies"]
            self.wallet = conf["wallet"]
            self.tickers = conf["tickers"]
