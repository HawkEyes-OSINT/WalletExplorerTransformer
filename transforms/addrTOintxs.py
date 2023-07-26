from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from addrMethods import Address


@registry.register_transform(display_name="In Transactions",
                             input_entity="maltego.BTCAddress",
                             description="Get input transactions from an address",
                             output_entities=["BTCTransaction"],
                             transform_set=WalletExplorer_set)
class addrTOintxs(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        # get address class
        try:
            addr = request.Value
            balance = request.getProperty('balance')
            incomingTXS = request.getProperty('incomingTXS')
            outgoingTXS = request.getProperty('outgoingTXS')
            address = Address(addr, balance, incomingTXS, outgoingTXS)
        except Exception as e:
            response.addUIMessage("Address not found", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
       # create address entity details
        if not balance or not incomingTXS or not outgoingTXS:
            ent = response.addEntity('maltego.BTCAddress', addr)
            ent.addProperty('balance', 'Balance', '', str(address.balance))
            ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(address.incomingTXS))
            ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(address.outgoingTXS))
 
        # get transaction list
        try:
            transactions = address.inputTransactions()
        except Exception as e:
            response.addUIMessage("Error getting transactions", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create transaction entities
        for transaction in transactions:
            ent = response.addEntity('maltego.BTCTransaction', transaction.trxID)
            ent.addProperty('date', 'Date', '', str(transaction.date))
            ent.addProperty('amount', 'Amount', '', str(transaction.amount))
            ent.setLinkThickness(2)
            ent.setLinkColor('#00FF00') # green
            ent.reverseLink()
    