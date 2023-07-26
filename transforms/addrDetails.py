from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from addrMethods import Address


@registry.register_transform(display_name="Address Details",
                             input_entity="maltego.BTCAddress",
                             description="Get details about a Bitcoin address.",
                             output_entities=["maltego.BTCAddress"],
                             transform_set=WalletExplorer_set)
class addrDetails(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        # get address details
        try:
            addr = request.Value    
            address = Address(addr)
        except Exception as e:
            response.addUIMessage('Could not find address', UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return  

        # create entity
        ent = response.addEntity("maltego.BTCAddress", addr)
        ent.addProperty('balance', 'Balance', '', str(address.balance))
        ent.addProperty('incomingTXS', 'Incoming Transactions', '', address.incomingTXS)
        ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', address.outgoingTXS)
        