# Import the Client class from the binance.client module to interact with the Binance API
from binance.client import Client


def get_accountbalance():

	# Create a new client object to interact with the Binance API
	client = Client("<<your_binance_api_key>>", "<<your_binance_secret_key>>")

	# Retrieve the balances of all coins in the user's Binance account
	balances = client.get_account()['balances']

	# Get the current price of all tickers from the Binance API
	all_tickers = client.get_all_tickers()

	# Create a dictionary of tickers and their corresponding prices
	list_tickers = {ticker['symbol']: float(ticker['price']) for ticker in all_tickers}

	# Calculate the USDT value of each coin in the user's account
	coins_usdt_value = []
	for balance in balances:
		# Get the asset symbol and the free and locked balance of each coin
		asset = balance['asset']
		free = float(balance['free'])
		locked = float(balance['locked'])

		# If the coin is USDT and the total balance is greater than 1, add it to the list of coins with their USDT values
		if asset == 'USDT' and free + locked > 1:
			coins_usdt_value.append(('USDT', (free + locked)))
		# Otherwise, check if the coin has a USDT trading pair or a BTC trading pair
		elif free + locked > 0.0:
			# Check if the coin has a USDT trading pair
			if (any(asset + 'USDT' in i for i in list_tickers)):
				# If it does, calculate its USDT value and add it to the list of coins with their USDT values
				symbol = asset + 'USDT'
				price = list_tickers.get(symbol)
				usdt_value = (free + locked) * price
				if usdt_value > 1:
					coins_usdt_value.append((asset, usdt_value)) 
			# If the coin does not have a USDT trading pair, check if it has a BTC trading pair
			elif (any(asset + 'BTC' in i for i in list_tickers)):
				# If it does, calculate its USDT value and add it to the list of coins with their USDT values
				symbol = asset + 'BTC'
				price = list_tickers.get(symbol)
				usdt_value = (free + locked) * price * list_tickers.get('BTCUSDT')
				if usdt_value > 1:
					coins_usdt_value.append((asset, usdt_value))
						  

	# Sort the list of coins and their USDT values by USDT value in descending order
	coins_usdt_value.sort(key=lambda x: x[1], reverse=True)

	# Return the list of coins and their USDT values
	return coins_usdt_value


def main():

	# Initialize the grand total USDT value to 0
	grand_usdt_total = 0

	# Call the get_accountbalance function to get the list of coins and their USDT values
	coins_usdt_value = get_accountbalance()

	# Print the list of coins and their USDT values in descending order of USDT value
	for coin, usdt_value in coins_usdt_value:
		print(f"{coin} : ${usdt_value:.2f}")
		# Add the USDT value of the current coin to the grand total USDT value
		grand_usdt_total += usdt_value

	# Print the grand total USDT value
	print(f"\nGrand Total: ${grand_usdt_total:.2f}")


if __name__ == '__main__':
	main()