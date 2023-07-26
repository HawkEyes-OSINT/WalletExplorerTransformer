from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from addrMethods import Address


@registry.register_transform(display_name="To Wallet",
                             input_entity="maltego.BTCAddress",
                             description="Get wallet information from address",
                             output_entities=["hawkdev.BitcoinWallet", 'maltego.BTCAddress'],
                             transform_set=WalletExplorer_set)
class addrTOwallet(DiscoverableTransform):

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
        
        # get wallet class
        try:
            wallet = address.toWallet()
        except Exception as e:
            response.addUIMessage("Wallet not found", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create address entity details
        if not balance or not incomingTXS or not outgoingTXS:
            ent = response.addEntity('maltego.BTCAddress', addr)
            ent.addProperty('balance', 'Balance', '', str(address.balance))
            ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(address.incomingTXS))
            ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(address.outgoingTXS))
        
        # create wallet entity
        ent = response.addEntity('hawkdev.BitcoinWallet', wallet.walletID)
        ent.addProperty('balance', 'Balance', '', str(wallet.balance))
        ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(wallet.incomingTXS))
        ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(wallet.outgoingTXS))
        ent.setLinkThickness(1)
