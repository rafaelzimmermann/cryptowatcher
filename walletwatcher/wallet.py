WALLET_EXODUS = 1
WALLET_BINANCE = 2
WALLET_CRYPTOCOM = 3
WALLET_DAEDALUS = 4

WALLETS = {
    1: 'Exodus',
    2: 'Binance',
    3: 'crypto.com',
    4: 'Daedalus'
}

WALLETS_PRECISION = {
    1: 8,
    2: 8,
    3: 8,
    4: 8
}


class Wallet:

    @staticmethod
    def wallet_name(wallet_id: int):
        return WALLETS[wallet_id]
