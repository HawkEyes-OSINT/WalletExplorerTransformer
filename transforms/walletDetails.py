from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from walletMethods import Wallet


@registry.register_transform(display_name="Wallet Details",
                             input_entity="hawkdev.BitcoinWallet",
                             description="Get details about a Bitcoin wallet.",
                             output_entities=["hawkdev.BitcoinWallet"],
                             transform_set=WalletExplorer_set)
class walletDetails(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        # get wallet details
        try:
            walletID = request.Value    
            wallet = Wallet(walletID)
        except Exception as e:
            response.addUIMessage('Could not find wallet', UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return  
        
       # create wallet entity
        ent = response.addEntity('hawkdev.BitcoinWallet', wallet.walletID)
        ent.addProperty('balance', 'Balance', '', str(wallet.balance))
        ent.addProperty('incomingTXS', 'Incoming Transactions', '', str(wallet.incomingTXS))
        ent.addProperty('outgoingTXS', 'Outgoing Transactions', '', str(wallet.outgoingTXS))
 