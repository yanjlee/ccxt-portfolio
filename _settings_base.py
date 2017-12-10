
# BITMEX_API_BASE = 'https://www.bitmex.com/api/v1/'

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

