import json

from model.portfolio import Portfolio 


class BalanceConfig:

    def __init__(self, manual_portifolio: Portfolio) -> None:
        self.manual_portifolio = manual_portifolio

    

class Config:

    def __init__(self, currency: str, balance_config: BalanceConfig):
        self.currency = currency
        self.balance_config = balance_config

    def to_json(self):
        data = {
            'currency': self.currency,
            'config': self.balance_config.manual_portifolio.to_dict()
        }
        return json.dumps(data)
