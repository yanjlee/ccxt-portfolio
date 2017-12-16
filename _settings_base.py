
from decimal import *

# Update this.
manual_btc_price = Decimal('18000')

## Insert any offline wallet balances or balances on Exchange currently down
manual_holding_entries = {
    # "Trezor":   [{"BTC": 10000.5}],
    # "Kraken":   [{"ETH": 1.00}], 
    # "Binance":  [{"THC": 500.00}],
    # "coins_in_transit":  [{"LTC": (9.5) }] # transactions in order. 
}

# Add in all deposits, subtract all withdrawals.
# Keys do not matter, number values will be summed.
# Adding each tx value will let you track your own history. 
total_deposits = {
    "coinbase": 1014.90 + 313+4301 + 918.49+1500  -1500-423.70 + 1525 + 1087
    # ,"gdax": 123 + 456
    ,"gemini": 10000
}

## Multiple accounts are supported for all exchanges. Use the same format shown for Bitmex.
bitmex_accounts = { 
    # "your_email+bitmex@gmail.com": {
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # },
    # "your_email+bitmex2@gmail.com": {
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # }
}

coinbase_accounts = {
    ## Use API Key with only 'read' permissions.
    ## If Coinbase gives you a '2 day delay' to enable your APIKey, its because you added transfer or trade permissions
    # "your_email@gmail.com": {
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # }
}

## GDAX: Use Read only API Key
gdax_accounts = {
    # "your_email@gmail.com": {
    #     "passphrase": "1357foo",
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # }
}

## Gemini: Use Fund Management API Key - This can withdraw to whitelisted IPs but can not trade.
## Do not enable any Whitelisted IPs to ensure that Key is not able to withdraw.
gemini_accounts = {
    # "your_email@gmail.com": {
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # }
}

bittrex_accounts = {
    # "your_email@gmail.com": {
    #     'API_KEY': 'abc123',
    #     'API_SECRET': 'efg1234_789'
    # }
}

