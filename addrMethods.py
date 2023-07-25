from supportMethods import MAX_CALLS, getSoup
from items import Wallet


"""
https://walletexplorer.com
methods to retreive details regarding Bitcoin addresses
"""

class Address:
    def __init__(self, addrID, balance=None, incomingTXS=None, outgoingTXS=None):
        """
        :input: address
        :output: balance, incomingTXS, outgoingTXS
        """
        self.addrID = addrID
        if not balance or not incomingTXS or not outgoingTXS:
            balance, incomingTXS, outgoingTXS = self._getDetails(addrID)
        self.balance = balance
        self.incomingTXS = incomingTXS
        self.outgoingTXS = outgoingTXS

    def _getDetails(self, addr):
        """
        :input: address
        :output: balance, incomingTXS, outgoingTXS
        :source: /address/{addrID} -> /wallet/{walletID}
        """
        # get address page
        url = f'https://walletexplorer.com/address/{addr}'
        soup = getSoup(url)

        # get total transaction count
        target_text = soup.find(text=lambda text: text and 'total transactions: ' in text)
        trx_total = int(target_text.text.split(': ')[1].split(')')[0].replace(',', ''))

        # extract wallet id and href for addr list
        target_text = soup.find('h2')
        href = target_text.a['href']
        walletID = href.split('/')[2]

        # extract pages to scan
        url = f'https://walletexplorer.com/wallet/{walletID}/addresses'
        soup = getSoup(url)
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # find addr in wallet
        page = 1
        target_text = []
        while page <= pages and page <= MAX_CALLS:
            # get relevant page
            url = f'https://walletexplorer.com/wallet/{walletID}/addresses?page={page}'
            soup = getSoup(url)
            page += 1

            # search for addr
            target_text = soup.select(f'tr:contains("{addr}")')
            if target_text:
                target_text = target_text[0]
                break
        if not target_text:
            return None, None, None
        
        # extract balance and incoming txs
        balance = float(target_text.find(class_='amount').text)
        incomingTXS = int(target_text.find(class_='amount').nextSibling.text)

        # calculate outgoing txs
        outgoingTXS = trx_total - incomingTXS

        return balance, incomingTXS, outgoingTXS

    def toWallet(self):
        """
        :input: address
        :output: wallet entity
        :source: /address/{addrId}
        """
        addr = self.addrID

        # get soup for wallet id
        url = f'https://walletexplorer.com//address/{addr}'
        soup = getSoup(url)

        # extract wallet id and href for addr list
        target_text = soup.find('h2')
        href = target_text.a['href']
        walletID = href.split('/')[2]

        # get soup for balance and addr list
        url = f'https://walletexplorer.com/wallet/{walletID}/addresses'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # extract balance and addr list
        page = 1
        balance = 0
        incomingTXS = 0
        while page <= pages:
            # get relevant page
            url = f'https://walletexplorer.com/wallet/{walletID}/addresses?page={page}'
            soup = getSoup(url)
            page += 1

            # extract balance and addr list
            target_text = soup.select('tr', class_='amount')[1:] # skip header row
            for target in target_text:
                if target != None:
                    balance += float(target.find(class_='amount').text)
                    incomingTXS += int(target.find(class_='amount').nextSibling.text)

        # get total transaction count
        url = f'https://walletexplorer.com/wallet/{walletID}'
        soup = getSoup(url)
        target_text = soup.find(text=lambda text: text and 'total transactions: ' in text)
        trx_total = int(target_text.text.split(': ')[1].split(')')[0].replace(',', ''))

        # caculate outgoing transactions
        outgoingTXS = trx_total - incomingTXS

        # create wallet entity
        wallet = Wallet(walletID, balance, incomingTXS, outgoingTXS)
        return wallet


    def outputTransactions(self):
        from transactionMethods import Transaction
        """
        :input: address
        :output: list of output transactions
        :source: /addresses/{addrID} -
        """
        addr = self.addrID

        # get soup
        url = f'https://walletexplorer.com/address/{addr}'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # iterate pages
        page = 1
        transactions_list = []
        while page <= pages:
            # get relevant page
            url = f'https://walletexplorer.com/address/{addr}?page={page}'
            page += 1
            soup = getSoup(url)
            transactions = soup.find_all('tr', {'class': 'sent'}) # get output transactions
            
            # extract date, amount, trid
            for transaction in transactions:
                txID = transaction.find(class_='txid').text.strip()
                date = transaction.find(class_='date').text.strip()
                amount = transaction.find(class_='amount').text.strip()
                transactions_list.append(Transaction(txID, date, amount))

        return transactions_list


    def inputTransactions(self):
        from transactionMethods import Transaction
        """
        :input: address
        :output: list of input transactions
        :source: /addresses/{addrID} +
        """
        addr = self.addrID

        # get soup
        url = f'https://walletexplorer.com/address/{addr}'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # iterate pages
        page = 1
        transactions_list = []
        while page <= pages:
            # get relevant page
            url = f'https://walletexplorer.com/address/{addr}?page={page}'
            page += 1
            soup = getSoup(url)
            transactions = soup.find_all('tr', {'class': 'received'}) # get output transactions
            
            # extract date, amount, trid
            for transaction in transactions:
                txID = transaction.find(class_='txid').text.strip()
                date = transaction.find(class_='date').text.strip()
                amount = transaction.find(class_='amount').text.strip()
                transactions_list.append(Transaction(txID, date, amount))

        return transactions_list


"""
Test Code
"""
# addr = Address('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4')
# print('Balance: ', addr.balance)
# print('Incoming TXs: ', addr.incomingTXS)
# print('Outgoing TXs: ', addr.outgoingTXS)
# print('Wallet: ', addr.toWallet())

# output_transactions = addr.outputTransactions()
# for transaction in output_transactions:
#     print('trxID', transaction.trxID)
#     print('date', transaction.date)
#     print('amount', transaction.amount)
#     print(' ')

# input_transactions = addr.inputTransactions()
# for transaction in input_transactions:
#     print('trxID', transaction.trxID)
#     print('date', transaction.date)
#     print('amount', transaction.amount)
#     print(' ')
