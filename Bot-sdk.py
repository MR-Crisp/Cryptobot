from Crypto.Cipher import AES #this is acting very wierd might have to replace
from getpass import getpass
import time
from alpaca.trading.client import TradingClient
from alpaca.data.requests import CryptoLatestQuoteRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

#these 4 imports are used to figure out the DCA of a symbol:
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

#For pretty printing
from pprint import pprint


def login():

    print("login")

def signup():
    username = input("username: ")
    while True:
        password = getpass("password: ")
        reconfirm = input("Re-enter password: ")
        if reconfirm == password:
            break
        else:
            print("password doesn't match")
    print(f'Hi there {username}, we just need your Key and s-Key')
    valid  = False
    while not valid:                    
        key = input("Key: ")
        skey = input("s-Key: ")
        valid = validate(key, skey)
    #plaintext = key + skey
    #safe_content = encrypt(password, plaintext)
    write_file(username,password,key,skey)

    print('You are good to go!')

        



def validate(key,skey): 
    try:
        acc = TradingClient(key,skey)
        valid = acc.get_account() 
        global client
        client = acc
        return True
    except:
        print('Error your Key or Secret Key are wrong')
        return False



    
def encrypt(key,plaintext): #putting this function in the back for now

    #key is password

    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(plaintext)

    return ciphertext

def decrypt(key,ciphertext): #putting this function in the back for now

    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def write_file(username,password,key,skey):


    with open('keys.txt','a') as f:
        f.write(f'{username}|{password}|{key}|{skey}\n')      



def buy_stock(client,symbol,qty):
    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
    return client.submit_order(order_data=market_order_data)

def buy_price(client,symbol,funds):
    current_price = coin_price(symbol)
    qty = funds/current_price
    qty = round(qty,3)
    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
    return client.submit_order(order_data=market_order_data)


def sell_marketprice(client,symbol,qty):
    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
    return client.submit_order(order_data=market_order_data)



def coin_price(symbol):
    cryptocoin = symbol
    price_checker = CryptoHistoricalDataClient()
    request_params = CryptoLatestQuoteRequest(symbol_or_symbols=cryptocoin)
    latest_quote = price_checker.get_crypto_latest_quote(request_params)
    latest_price = latest_quote[cryptocoin].ask_price
    return latest_price



def details(client):
    account = client.get_account()
    answer = input('Account ID, Balance, Portfolio value, Buying power, All of the above')


    if answer == 'Account ID':
        print(f'Account ID:  {account.id}')
    if answer == 'BAL':
        print(f'BAL:  {account.cash}')
    if answer == 'Portfolio Value':
        print("Portfolio Value:", account.portfolio_value)
    if answer == 'Buying Power':
        print("Buying Power:", account.buying_power)
    if answer == 'All of the above':
        print("Account ID: ", account.id)
        print(f'BAL:  {account.cash}')
        print("Portfolio Value:", account.portfolio_value)
        print("Buying Power:", account.buying_power)
        


def average_symbol_value(symbol,days):
    client = CryptoHistoricalDataClient()

    end = datetime.utcnow()
    start = end - timedelta(days=days)

    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=start.isoformat(),
        end=end.isoformat()
    )
    bars = client.get_crypto_bars(request_params)
    
    prices = [bar.close for bar in bars[symbol]]
    avg = sum(prices) / len(prices)
    return avg


def DCA_logic():
    
    market_price = coin_price('BTC/USD')
    inital_buyInPrice = 0
    target_price = 0


 
#signup()


client = 0


#key ='PKMS1S5M1C60839ET2QC' 
#skey='YaXCd0ItTQUPwFwPcRECyQs71UnuPlqnHhPZFjWR'

#signup()

print(average_symbol_value('BTC/USD',33))
