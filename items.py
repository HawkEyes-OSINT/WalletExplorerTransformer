"""
class entities to be used by methods
"""




class Wallet:
    def __init__(self, walletID, balance, incomingTXS, outgoingTXS):
        self.walletID = walletID
        self.balance = balance
        self.incomingTXS = incomingTXS
        self.outgoingTXS = outgoingTXS



