from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from transactionMethods import Transaction


@registry.register_transform(display_name="To Input Wallet",
                             input_entity="maltego.BTCTransaction",
                             description="Get input wallet of transaction",
                             output_entities=["hawkdev.BitcoinWallet"],
                             transform_set=WalletExplorer_set)
class trxTOinwallet(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        try:
            trxID = request.Value
            date = request.getProperty('date')
            amount = request.getProperty('amount')
            trx = Transaction(trxID, date, amount)
        except Exception as e:
            response.addUIMessage("Error: Could not find transaction", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create transaction entity details
        if not date or not amount:
            ent = response.addEntity("maltego.BTCTransaction", trxID)
            ent.addProperty('date', 'Date', '', str(trx.date))
            ent.addProperty('amount', 'Amount', '', str(trx.amount)) 

        # get input addresses
        try:
            wallet_dict = trx.toInputWallet()
        except Exception as e:
            response.addUIMessage("Error: Could not find input wallet", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create input wallet entity
        wallet = wallet_dict['wallet']
        ent = response.addEntity("hawkdev.BitcoinWallet", wallet.walletID)
        ent.addProperty('balance', 'Balance', '', str(wallet.balance))
        ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(wallet.incomingTXS))
        ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(wallet.outgoingTXS))
        ent.setLinkLabel(str(wallet_dict['amount']))
        ent.reverseLink()
        ent.setLinkThickness(2)
        ent.setLinkColor('#FF0000') # red
       