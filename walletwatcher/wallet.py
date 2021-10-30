WALLET_EXODUS = 1

WALLETS = {
    1: 'Exodus'
}

WALLETS_PRECISION = {
    1: 8
}


class Wallet:

    @staticmethod
    def wallet_name(wallet_id: int):
        return WALLETS[wallet_id]
