from supportMethods import MAX_CALLS, getSoup


"""
https://walletexplorer.com
methods to retreive details regarding Bitcoin transactions
"""

class Wallet:
    def __init__(self, walletID, balance=None, incomingTXS=None, outgoingTXS=None):
        if not balance or not incomingTXS or not outgoingTXS:
            balance, incomingTXS, outgoingTXS = self._getDetails(walletID)
        self.walletID = walletID
        self.balance = balance
        self.incomingTXS = incomingTXS
        self.outgoingTXS = outgoingTXS

    
    def _getDetails(self, walletID):
        """
        gets details regarding a wallet
        :param WalletID: walletID of wallet to retreive details for
        :return: balance, incomingTXS, outgoingTXS
        :source: /wallet/{walletID}/addresses
        """
        balance, incomingTXS, outgoingTXS = 0, 0, 0
        # get soup
        url = f'https://walletexplorer.com/wallet/{walletID}/addresses'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # calculate balance and incomingTXS
        page = 1
        while page <= pages and page <= MAX_CALLS:
            # get relevant page
            url = f'https://walletexplorer.com/wallet/{walletID}/addresses?page={page}'
            soup = getSoup(url)
            page += 1
            
            target_text = soup.select('tr', class_='amount')[1:] # remove title line
            for target in target_text:
                balance += float(target.find(class_='amount').text.strip())
                incomingTXS += int(target.find(class_='amount').next.next.text)

        # get soup for total transactions
        url = f'https://walletexplorer.com/wallet/{walletID}'
        soup = getSoup(url)

        # extract total transactions
        totalTXS = soup.find('small', string=lambda string: string and 'total transactions:' in string.lower())
        totalTXS = int(totalTXS.text.split(' ')[2].split(')')[0].replace(',', ''))

        # calculate outgoingTXS
        outgoingTXS = totalTXS - incomingTXS

        return balance, incomingTXS, outgoingTXS
    
    # incomplete
    def ouputTransactions(self):
        from transactionMethods import Transaction
        """
        gets all outgoing transactions for a wallet
        :return: list of transactions
        :source: /wallet/{walletID}
        """
        transaction_list = []
        # extract soup
        walletID = self.walletID
        url = f'https://walletexplorer.com/wallet/{walletID}'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # extract transaction data
        page = 1
        while page <= pages and page <= MAX_CALLS:
            # get relevant page
            url = f'https://walletexplorer.com/wallet/{walletID}?page={page}'
            soup = getSoup(url)
            page += 1
            
            # get ouptut transactions
            target_text = soup.findAll('tr', class_='sent')
            for target in target_text:
                # get trxID and date
                trxID = target.find('td', class_='txid').a['href'].split('/')[2]
                date = target.find('td', class_='date').text.strip()

                # calculate transaction amound
                amount = 0
                amount_list = target.findAll('td', class_='amount')[:-1]
                for amount_text in amount_list:
                    if '(' in amount_text.text: # fee
                            amount += float(amount_text.text.strip().split('(')[1].split(')')[0])
                    else:
                        amount += float(amount_text.text.strip())

                # inster transaction to list
                trx = Transaction(trxID, date=date, amount=amount*(-1))
                transaction_list.append(trx)

        return transaction_list
    
    # incomplete
    def inputTransactions(self):
        from transactionMethods import Transaction
        """
        gets all incoming transactions for a wallet
        :return: list of transactions
        """
        transaction_list = []
        # extract soup
        walletID = self.walletID
        url = f'https://walletexplorer.com/wallet/{walletID}'
        soup = getSoup(url)

        # extract pages to scan
        target_text = soup.find(class_='paging')
        pages = int(target_text.text.split('/ ')[1].split(' ')[0])

        # extract transaction data
        page = 1
        while page <= pages and page <= MAX_CALLS:
            # get relevant page
            url = f'https://walletexplorer.com/wallet/{walletID}?page={page}'
            soup = getSoup(url)
            page += 1
            
            # get ouptut transactions
            target_text = soup.findAll('tr', class_='received')
            for target in target_text:
                # get trxID and date
                trxID = target.find('td', class_='txid').a['href'].split('/')[2]
                date = target.find('td', class_='date').text.strip()

                # calculate transaction amound
                amount = 0
                amount = float(target.find('td', class_='amount').text.strip())

                # inster transaction to list
                trx = Transaction(trxID, date=date, amount=amount)
                transaction_list.append(trx)

        return transaction_list
    

"""
Test Code
"""

# walletID = '047e9f4d9e910d7d'
# wallet = Wallet(walletID)

# # getDetails
# print('balance: ', wallet.balance)
# print('incomingTXS: ', wallet.incomingTXS)
# print('outgoingTXS: ', wallet.outgoingTXS)

# getOutputTransactions
# outTRXS = wallet.ouputTransactions()
# for trx in outTRXS:
#     print('trxID: ', trx.trxID)
#     print('date: ', trx.date)
#     print('amount: ', trx.amount)
#     print()

# # getInputTransactions
# inTRXS = wallet.inputTransactions()
# for trx in inTRXS:
#     print('trxID: ', trx.trxID)
#     print('date: ', trx.date)
#     print('amount: ', trx.amount)
#     print()