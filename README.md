### WelletExplorerTransformer
Graph crypto transactions between addresses and wallets

## Download and Installation
To download the repository, open a command line in the directory in which you woul like to store the repository and run:
    git clone https://github.com/HawkEyes-OSINT/WalletExplorerTransformer.git

Install the requirements:
    pip install -r requirements.txt

To import the transforms into your Maltego client, proceed as follows:

Open your Maltego client and navigate to the 'Import/Export' tab.
Click on 'Import Config.'
Select the file 'WalletExplorer.mtz.'

## Transform and Methods Outline
## walletexplorer.com

# addr methods
toWallet:
	input: addr
	output: wallet /wallet/{walletID}/d/addresses 
		properties: wallet balance sum(balance)
			 addr in wallet
	link: 1
getDetails:
	input: addr
	output: addr /address/{addrID} -> /wallet/{walletID}
		properties: balance
			incoming_transactions
			outgoing_transactions
outputTransactions:
	input: addr
	output: trx /addresses/{addrID} -
		properties: date
			amount
	link: 2, red
inputTransactions:
	input: addr
	output: trx /addresses/{addrID} +
		properties: date
			amount
	link: 2, reverse, green


# transaction methods
getDetails:
	input: transactionID
	output: transactionID /txid/{txID}
		properties: block
			time
			fee
toInputAddr:
	input: transactionID
	output: addr
		properties: addr -> getDtails
	link: 2, red, amount
toOutputAddr:
	input: transactionID
	output: addr
		properties: addr -> getDetails
	link: 2, green, amount
toInputWallet:
	input: transactionID
	output: wallet
		properties: wallet balance
			addr in wallet
	link: 2, red, revers, amount
toOutputWallet:
	input: transationID
	output: wallet
		properties: wallet balance
		addr in wallet
	link: 2, green, amount

# wallet methods
getDetails:
	input: wallet /wallet/{walletID}/addresses
	output wallet
		properties: balance sum(balance)
			addr
outputTransactions:
	input: wallet /wallet/{walletID}
	output: trx
		properties: date
			amount sum(sent)
	link: 2, red
inputTransactions:
	input: wallet /wallet/{walletID}
	output: trx
		properties: date
			amount
	link: 2, reverse, green

