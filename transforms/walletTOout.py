from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from walletMethods import Wallet


@registry.register_transform(display_name="Output Transactions",
                             input_entity="hawkdev.BitcoinWallet",
                             description="Get output transactions for a wallet",
                             output_entities=["maltego.BTCTransaction"],
                             transform_set=WalletExplorer_set)
class walletTOout(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        # get wallet details
        try:
            walletID = request.Value    
            wallet = Wallet(walletID)
            balance = wallet.balance
            incomingTXS = wallet.incomingTXS
            outgoingTXS = wallet.outgoingTXS
        except Exception as e:
            response.addUIMessage('Could not find wallet', UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return  
        
        # create wallet entity
        if not balance or not incomingTXS or not outgoingTXS:
            ent = response.addEntity('hawkdev.BitcoinWallet', wallet.walletID)
            ent.addProperty('balance', 'Balance', '', str(wallet.balance))
            ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(wallet.incomingTXS))
            ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(wallet.outgoingTXS))
 
        # get transaction list
        try:
            transactions = wallet.ouputTransactions()
        except Exception as e:
            response.addUIMessage('Could not find transactions', UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create transaction entities
        for transaction in transactions:
            ent = response.addEntity('maltego.BTCTransaction', transaction.trxID)
            ent.addProperty('date', 'Date', '', str(transaction.date))
            ent.addProperty('amount', 'Amount', '', str(transaction.amount))
            ent.setLinkLabel(str(transaction.amount))
            ent.setLinkThickness(2)
            ent.setLinkColor('#FF0000') # red
