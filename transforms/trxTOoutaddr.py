from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from transactionMethods import Transaction


@registry.register_transform(display_name="To Output Addr",
                             input_entity="maltego.BTCTransaction",
                             description="Get output addresses of transaction",
                             output_entities=["maltego.BTCAddress"],
                             transform_set=WalletExplorer_set)
class trxTOoutaddr(DiscoverableTransform):

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
            addr_list = trx.toOutputAddr()
        except Exception as e:
            response.addUIMessage("Error: Could not find input addresses", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return

        # create address entities
        for address in addr_list:
            addr = address['addr']
            ent = response.addEntity("maltego.BTCAddress", addr.addrID)
            ent.addProperty('balance', 'Balance', '', str(addr.balance))
            ent.addProperty('incomingTXS', 'Incoming Transactions', '', addr.incomingTXS)
            ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', addr.outgoingTXS)
            ent.setLinkLabel(str(address['amount']))
            ent.setLinkThickness(2)
            ent.setLinkColor('#00FF00') # green
