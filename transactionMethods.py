from supportMethods import getSoup


"""
https://walletexplorer.com
methods to retreive details regarding Bitcoin transactions
"""

class Transaction:
    def __init__(self, trxID, date=None, amount=None):
        """
        :param trxID: transaction ID
        :param date: date of transaction
        :param amount: amount of transaction
        """
        from addrMethods import Address
        from items import Wallet

        if not date or not amount:
            date, amount = self._getDetails(trxID)        
        self.trxID = trxID
        self.date = date
        self.amount = amount

    # incomplete
    def _getDetails(self, trxID):
        """
        get transaction details
        :return: date, amount
        """
        date = ''
        amount = ''

        # get soup
        url = f'https://walletexplorer.com/txid/{tid}'
        soup = getSoup(url)

        # extract date
        time = soup.find('th', text='Time')
        date = time.find_next_sibling('td').text.strip()

        # extract amount
        amount = soup.find(class_='tx')
        amount = amount.text.strip()
        amount = amount.split('(')[1].split(' ')[0].strip()

        return date, amount
    

    # incomplete
    def toInputAddr(self):
        """
        get input address
        :return: input address
        """
        addr = ''
        return addr


    # incomplete
    def toOutputAddr(self):
        """
        get output address
        :return: output address
        """
        addr = ''
        return addr
    

    # incomplete
    def toInputWallet(self):
        """
        get input wallet
        :return: input wallet
        """
        wallet = ''
        return wallet
    

    # incomplete
    def toOutputWallet(self):
        """
        get output wallet
        :return: output wallet
        """
        wallet = ''
        return wallet
    

"""
Test Code
"""
tid = 'e64647ba5bd13e7e0214ef1554456103643b84dd00e51b0fc718bd07fe3b8e51'
transaction = Transaction(tid)
print('tid: ', transaction.trxID)
print('date: ', transaction.date)
print('amount: ', transaction.amount)
