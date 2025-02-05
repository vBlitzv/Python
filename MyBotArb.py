import time
from v4_client_py.clients import IndexerClient, Subaccount
from v4_client_py.clients.constants import Network
from v4_client_py.clients.helpers import OrderBuilder

def initialize_client():
    """Initialize the dYdX client with testnet configuration."""
    return IndexerClient(config=Network.testnet().indexer_config)

def authenticate_subaccount(mnemonic):
    """Authenticate the subaccount using mnemonic phrase."""
    subaccount = Subaccount.from_mnemonic(mnemonic)
    return subaccount, subaccount.address

def get_market_data(client):
    """Fetch market data from dYdX."""
    markets_response = client.markets.get_markets()
    return markets_response.data['markets']

def find_arbitrage_opportunities(markets):
    """Analyze market data to detect arbitrage opportunities with cross-exchange comparisons."""
    opportunities = []
    for market, data in markets.items():
        bid_price = float(data['best_bid']) if data['best_bid'] else None
        ask_price = float(data['best_ask']) if data['best_ask'] else None
        
        # Fetch additional exchange data (Placeholder for real implementation)
        external_bid_price = bid_price * 1.002  # Example: external exchange bid slightly higher
        external_ask_price = ask_price * 0.998  # Example: external exchange ask slightly lower
        
        # Identify arbitrage opportunities across dYdX and external sources
        if bid_price and ask_price and bid_price > ask_price * 1.001:
            opportunities.append((market, bid_price, ask_price))
        elif external_bid_price and external_ask_price and external_bid_price > external_ask_price * 1.001:
            opportunities.append((market, external_bid_price, external_ask_price))
    
    return opportunities

def execute_trade(client, subaccount, market, side, size, price):
    """Place a trade order on dYdX with error handling."""
    order = OrderBuilder(
        subaccount=subaccount,
        market=market,
        side=side,
        type='limit',
        size=str(size),
        price=str(price),
        time_in_force='gtc'
    ).build()
    
    try:
        response = client.orders.place_order(order)
        return response
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def main():
    """Main loop for the arbitrage bot."""
    mnemonic = "orange noodle attack hungry account scout guide hover cluster rocket glass fossil novel reward caution glad pizza artefact vessel prepare retreat girl oil firm"
    client = initialize_client()
    subaccount, address = authenticate_subaccount(mnemonic)
    
    while True:
        print("Fetching market data...")
        markets = get_market_data(client)
        opportunities = find_arbitrage_opportunities(markets)
        
        for market, bid, ask in opportunities:
            print(f"Arbitrage Opportunity: {market} - Buy at {ask}, Sell at {bid}")
            execute_trade(client, subaccount, market, 'buy', 0.01, ask)
            execute_trade(client, subaccount, market, 'sell', 0.01, bid)
        
        # Dynamic wait time based on market activity
        wait_time = max(1, min(10, len(opportunities) * 2))  # Adjust between 1s and 10s
        print(f"Waiting {wait_time} seconds before next check...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
