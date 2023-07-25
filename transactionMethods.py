from supportMethods import MAX_CALLS, getSoup


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
        time = soup.find('th', string='Time')
        date = time.find_next_sibling('td').text.strip()

        # extract amount
        amount = soup.find(class_='tx')
        amount = amount.text.strip()
        amount = amount.split('(')[1].split(' ')[0].strip()

        return date, amount
    

    
    def toInputAddr(self):
        from addrMethods import Address
        """
        get input address
        :return: list of dictionaries with input addresses and amounts
        """
        addr_list = []

        # get soup
        trid = self.trxID
        url = f'https://walletexplorer.com/txid/{trid}'
        soup = getSoup(url)

        # get input count
        input_count = soup.find('b').text.strip()
        input_count = int(input_count.split(' ')[1])

        # extract input addresses
        target_text = soup.findAll('a', href=lambda href: href and href.startswith('/address/'))
        input_addresses = [addr for addr in target_text[:input_count]]
        if len(input_addresses) > MAX_CALLS:
            return addr_list
        for addr in input_addresses:
            address = Address(addr.text.strip())
            amount = addr.next.next.text.strip()
            addr_list.append({'addr': address, 'amount': amount})

        return addr_list


    
    def toOutputAddr(self):
        from addrMethods import Address
        """
        get output address
        :return: output address, amount
        """
        addr_list = []

        # get soup
        trid = self.trxID
        url = f'https://walletexplorer.com/txid/{trid}'
        soup = getSoup(url)

        # get input count
        input_count = soup.find('b').text.strip()
        input_count = int(input_count.split(' ')[1])

        # extract output addresses
        target_text = soup.findAll('a', href=lambda href: href and href.startswith('/address/'))
        output_addresses = [addr for addr in target_text[input_count:]]
        if len(output_addresses) > MAX_CALLS:
            return addr_list
        for addr in output_addresses:
            address = Address(addr.text.strip())
            amount = addr.next.next.next.next.next.next.text.strip()
            amount = amount.replace('\xa0', '')
            if amount[-3:] == 'BTC':
                addr_list.append({'addr': address, 'amount': amount})

        return addr_list
    

    def toInputWallet(self):
        from items import Wallet
        """
        get input wallet
        :return: input wallet, amount
        """
        # get soup
        trid = self.trxID
        url = f'https://walletexplorer.com/txid/{trid}'
        soup = getSoup(url)

        # extract wallet
        target_text = soup.find('a', href=lambda href: href and href.startswith('/wallet/'))
        wallet = target_text['href'].split('/')[-1]
        wallet = Wallet(wallet)

        # extract amount
        amount = soup.find('span', style='font-weight: normal;')
        amount = amount.text.split('(')[1].split(')')[0]

        return {'wallet': wallet, 'amount': amount}
    

    def toOutputWallet(self):
        from items import Wallet
        """
        get output wallet
        :return: input wallet, amount
        """
        wallet_list = []

        # get soup
        trid = self.trxID
        url = f'https://walletexplorer.com/txid/{trid}'
        soup = getSoup(url)

        # extract wallet and amount
        target_text = soup.findAll('a', href=lambda href: href and href.startswith('/wallet/'))[1:]
        if len(target_text) > MAX_CALLS:
            return wallet_list
        for target in target_text:
            wallet = target['href'].split('/')[-1]
            amount = target.next.next.next.text.strip()
            amount = amount.replace('\xa0', '')
            wallet_list.append({'wallet': Wallet(wallet), 'amount': amount})
        
        return wallet_list
    

"""
Test Code
"""
tid = '5dd65f6a00f982e7bc03d97c342b3826dcf37273e9efbf4aa210fc68168969e5'
transaction = Transaction(tid)

# # getDetails
# print('tid: ', transaction.trxID)
# print('date: ', transaction.date)
# print('amount: ', transaction.amount)

# # toInputAddr
# input_addr = transaction.toInputAddr()
# for addr in input_addr:
#     print(addr)

# # toOutputAddr
# output_addr = transaction.toOutputAddr()
# for addr in output_addr:
#     print(addr)

# # toInputWallet
# input_wallet = transaction.toInputWallet()
# print(input_wallet)

# # toOutputWallets
# output_wallets = transaction.toOutputWallet()
# for wallet in output_wallets:
#     print(wallet)
