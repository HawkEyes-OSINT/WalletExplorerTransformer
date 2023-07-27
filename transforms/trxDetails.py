from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
from extensions import registry, WalletExplorer_set
from transactionMethods import Transaction


@registry.register_transform(display_name="Transaction Details",
                             input_entity="maltego.BTCTransaction",
                             description="Get details regarding BTC transaction",
                             output_entities=["maltego.BTCTransaction"],
                             transform_set=WalletExplorer_set)
class trxDetails(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        try:
            trxID = request.Value
            trx = Transaction(trxID)
        except Exception as e:
            response.addUIMessage("Could not find transaction", UIM_PARTIAL)
            response.addUIMessage(str(e), UIM_PARTIAL)
            return
        
        # create entity
        ent = response.addEntity("maltego.BTCTransaction", trxID)
        ent.addProperty('date', 'Date', '', trx.date)
        ent.addProperty('amount', 'Amount', '', trx.amount) 
