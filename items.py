"""
class entities to be used by methods
"""




class Wallet:
    def __init__(self, walletID, balance, incomingTXS, outgoingTXS):
        self.walletID = walletID
        self.balance = balance
        self.incomingTXS = incomingTXS
        self.outgoingTXS = outgoingTXS


class Transaction:
    def __init__(self, trxID, date=None, amount=None):
        self.trxID = trxID
        self.date = date
        self.amount = amount
