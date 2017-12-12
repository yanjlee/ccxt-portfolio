
import argparse
import json
import csv
import sys
import time
from decimal import *

from settings import bitmex_accounts, gdax_accounts, coinbase_accounts, gemini_accounts, bittrex_accounts
from settings import total_deposits, manual_holding_entries
# Coinbase
from coinbase.wallet.client import Client as CB_Client

import ccxt

# Using an array will allow the summation of accounts across people and emails
# Potentially useful for Fund-level accounting or summing portfolio of partners

class CryptoPortfolio:
    def __init__(self):

        self.portfolio_info = manual_holding_entries
        self.portfolio_info.update({
            "Bitmex":   [],
            "Gemini":   [],
            "Coinbase": [],
            "GDAX":     [],
            "Bittrex":  []
        })
        
        self.bitmex     = None # Using multiple accounts will leave the last Conn assigned here
        self.bittrex    = None  
        self.cb_client  = None
        self.gdax       = None
        self.gemini     = None

        self.bitmex_margin_stake = Decimal(0)
            
        self.load_bitmex_accounts()
        self.load_coinbase_accounts()
        self.load_gdax_accounts()
        self.load_gemini_accounts()
        self.load_bittrex_accounts()

    def insert_portfolio_object(self, exchange, obj):
        if type(obj) == list: # ["GDAX", "Coinbase", "Gemini"]
            self.portfolio_info[exchange] += obj # Add {}s from []
        elif type(obj)==dict:
            self.portfolio_info[exchange].append( obj ) # Insert {} to []
        else:
            raise Exception("Invalid portfolio/account object passed to insert_portfolio_object")

    # Load Bitmex Account
    def load_bitmex_accounts(self):
        for account_email, config in bitmex_accounts.iteritems():
            self.bitmex     = ccxt.bitmex({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # BitmexConnection = bitmex.BitMEX(base_url=BITMEX_API_BASE, apiKey=config['API_KEY'], apiSecret=config['API_SECRET'])
            # account_data = BitmexConnection.get_account_info() # returns {}

            balance = self.bitmex.fetchBalance()
            # Use all info here, want to see what is open on margins
            summary = {'BTC': balance['BTC'] }

            self.insert_portfolio_object('Bitmex', summary) 
            # print json.dumps(balance,  indent=2)

    def load_bittrex_accounts(self):
        for account_email, config in bittrex_accounts.iteritems():
            self.bittrex    = ccxt.bittrex({'verbose': False, 'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})           
            # USDT will show up in this balance, but not in B wallets UI in bittrex
            balances = self.bittrex.fetchBalance() 
            balance_totals = balances['total'] # Keyed on coin
            for coin in balance_totals.keys():
                if balance_totals[coin] == 0:
                    del balance_totals[coin]

            self.insert_portfolio_object('Bittrex', balance_totals)

    # https://github.com/coinbase/coinbase-python
    # https://developers.coinbase.com/blog/2015/01/20/official-python-support
    def load_coinbase_accounts(self):
        for account_email, config in coinbase_accounts.iteritems():
            self.cb_client  = CB_Client(config['API_KEY'], config['API_SECRET'])
            cb_accounts = self.cb_client.get_accounts()['data'] # cb.Account Classes []

            summary = {}
            for acct in cb_accounts:
                curr = acct['balance']['currency']
                amount = acct['balance']['amount']
                summary[ curr ] = amount

            self.insert_portfolio_object('Coinbase', summary) 

            ## CCXT does *not* support coinbase
            # coinbase = ccxt.coinbase({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # balances = coinbase.fetchBalance()
            # summary = balances['total']

    def load_gdax_accounts(self):
        for account_email, config in gdax_accounts.iteritems():
            self.gdax       = ccxt.gdax({'apiKey':config['API_KEY'], 'secret':config['API_SECRET'], 'password':config['passphrase']})
            
            balances = self.gdax.fetchBalance()
            summary = balances['total']

            self.insert_portfolio_object('GDAX', summary)
            # print json.dumps(accounts, indent=2)r

    def load_gemini_accounts(self):
        for account_email, config in gemini_accounts.iteritems():
            self.gemini     = ccxt.gemini({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
        
            balances = self.gemini.fetchBalance()
            summary = balances['total']

            self.insert_portfolio_object('Gemini', summary)
            # print json.dumps(balances, indent=2)

    def get_sum_balances(self):
        sums = {}
        for exchange in PV.portfolio_info.keys():
            for account in PV.portfolio_info[exchange]:
                for coin in account.keys():

                    try:
                        # Don't count Leveraged Margin on Bitmex
                        if exchange=="Bitmex":
                            print "Not counting Bitmex margin stakes: "+str(account[coin]['used'])
                            self.bitmex_margin_stake += self.str_to_XBT( str(account[coin]['used']) )
                            coin_val = self.str_to_XBT( account[coin]['free'] )
                        else:
                            coin_val = self.str_to_XBT( account[coin] )

                        if coin in sums: 
                            sums[coin] += coin_val
                        else: 
                            sums[coin] = coin_val
                    except Exception, e:
                        import pdb; pdb.set_trace()


        return sums

    @staticmethod
    def print_sums(sums):
        string_objs = {}
        for key in sums.keys():
            string_objs[key] = str(sums[key])
        print json.dumps( string_objs,  indent=2)

    @staticmethod
    def str_to_XBT(XBT_str):
        return Decimal( XBT_str ).quantize(Decimal('.00000001'))

    def get_btc_usd_totals(self, balances):
        btc_total = Decimal(0)
        usd_total = Decimal(0)
        for key in balances.keys():
            if key=="BTC":
                btc_total += balances[key]
                # import pdb; pdb.set_trace()
                print "*%s: %s" % (key.rjust(4), str( round(balances[key],3)))
            elif key=="USD":
                usd_total += balances[key]
            elif key=="USDT":
                usd_total += balances[key]
            else:
                ticker = key+"/BTC"  # E.g. "ETH/BTC"
                bittrex_btc_rate = self.str_to_XBT( self.bittrex.fetchTicker(ticker)['last'] )
                btc_value = balances[key] * bittrex_btc_rate

                bittrex_btc_rate_str = "%.8f" %  bittrex_btc_rate
                btc_value_str = "%.8f" %  btc_value
                print "%s: %s at %s BTC each is worth %s BTC" % (key.rjust(5), str(round(balances[key],2)).rjust(10), bittrex_btc_rate_str, btc_value_str)
                btc_total+=btc_value

        return btc_total, usd_total

## ToDo: Trade history profit calculations
# class CryptoTradeHistory(CryptoPortfolio):
#     def __init__(self):
#         pass

#     def test(self):
#         print "Hi"
#         print "PV.portfolio_info"
#         pass

if __name__ == "__main__":

    PV = CryptoPortfolio()
    balances = PV.get_sum_balances() 

    try:
        print "\n\nYour holdings in each account are: "
        print json.dumps(PV.portfolio_info,  indent=2)


        print "\n\nYour summed holdings for each currency are: "
        btc_total, usd_total = PV.get_btc_usd_totals(balances)
        # btc_price = Decimal('13500') # Placeholder value while BTC swings wildly on Dec 9th
        btc_price = PV.str_to_XBT( PV.bittrex.fetchTicker('BTC/USDT')['last'] )

        btc_usd_value = (btc_total * btc_price) 
        portfolio_value = btc_usd_value + usd_total

        print "\n\n Your total Portfolio Value is estimated at: "
        print "%s BTC: ($%d) + $%d => %d" %( "%.3f"%btc_total, btc_usd_value, usd_total, portfolio_value)
        print "This is using a BTC value of %d" % (btc_price)

        total_deposits = sum( total_deposits.values() )
        profits = portfolio_value- Decimal(total_deposits)
        print "\n\n Your total USD Deposits have been: $%d" % (total_deposits)
        print "This yields a total profit of: ** $%d **" % (profits)
        if PV.bitmex_margin_stake > 0:
            staked_usd = btc_price*PV.bitmex_margin_stake
            print "Currently staked bitmex margin is %d, ($%d) for profit of $%d" % (PV.bitmex_margin_stake, staked_usd, profits+staked_usd)

        print "\n\nThis is based on current holdings and price of those holdings when converted to BTC."
        print "So it is net of all transaction fees\n"
        
        ## Print holdings on each Exchange
        # print json.dumps(PV.portfolio_info,  indent=2)
        # PV.print_sums( balances )

    except Exception, e:
        import pdb; pdb.set_trace()



