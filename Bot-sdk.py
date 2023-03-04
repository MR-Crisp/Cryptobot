from Crypto.Cipher import AES #this is acting very wierd might have to replace
from getpass import getpass
from time import sleep
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

def signup()->None:
    """
    Prompts the user to enter a username, password, and Alpaca API Key and Secret Key. 
    Verifies the keys are valid and writes the user's information to a file.
    """
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


def validate(key: str, skey: str) -> bool:
    """
    Attempts to create a TradingClient object using the provided API Key and Secret Key. 
    Returns True if successful, False otherwise.
    
    Args:
        key (str): Alpaca API Key.
        skey (str): Alpaca Secret Key.
    
    Returns:
        bool: True if the TradingClient object was successfully created, False otherwise.
    """

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

def write_file(username: str, password: str, key: str, skey: str) -> None:

    """
    Writes a user's information to a file in the format "username|password|key|skey".
    
    Args:
        username (str): The user's chosen username.
        password (str): The user's chosen password.
        key (str): The user's Alpaca API Key.
        skey (str): The user's Alpaca Secret Key.
    """

    with open('keys.txt','a') as f:
        f.write(f'{username}|{password}|{key}|{skey}\n')      


def buy_stock(client: TradingClient, symbol: str, qty: float) -> dict:
    """
    Places a market order to buy a specified quantity of a given cryptocurrency symbol.
    
    Args:
        client (TradingClient): The Alpaca TradingClient object.
        symbol (str): The cryptocurrency symbol to buy.
        qty (float): The quantity of the cryptocurrency to buy.
    
    Returns:
        dict: The response from the Alpaca API containing information about the submitted order.
    """


    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
    return client.submit_order(order_data=market_order_data)

def buy_price(client: TradingClient, symbol: str, funds: float) -> dict:

    """
    Places a market order to buy as much of a given cryptocurrency symbol as possible with a specified amount of funds.
    
    Args:
        client (TradingClient): The Alpaca TradingClient object.
        symbol (str): The cryptocurrency symbol to buy.
        funds (float): The amount of funds to use to buy the cryptocurrency.
    
    Returns:
        dict: The response from the Alpaca API containing information about the submitted order.
    """
    current_price = coin_price(symbol)
    qty = funds/current_price
    qty = round(qty,3)
    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force='gtc'
                    )
    return client.submit_order(order_data=market_order_data),qty

def sell_marketprice(client: TradingClient, symbol: str, qty: float) -> dict:

    """
    Places a market order to sell a specified quantity of a given cryptocurrency symbol.
    
    Args:
        client (TradingClient): The Alpaca TradingClient object.
        symbol (str): The cryptocurrency symbol to sell.
        qty (float): The quantity of the cryptocurrency to sell.
    
    Returns:
        dict: The response from the Alpaca API containing information about the submitted order.
    """
    market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
    return client.submit_order(order_data=market_order_data)


def coin_price(symbol: str) -> float:

    """
    Retrieves the current price of a specified cryptocurrency symbol.
    
    Args:
        symbol (str): The cryptocurrency symbol to retrieve the price for.
    
    Returns:
        float: The current price of the specified cryptocurrency symbol.
    """
    cryptocoin = symbol
    price_checker = CryptoHistoricalDataClient()
    request_params = CryptoLatestQuoteRequest(symbol_or_symbols=cryptocoin)
    latest_quote = price_checker.get_crypto_latest_quote(request_params)
    latest_price = latest_quote[cryptocoin].ask_price
    return latest_price


def details(client):
    """
    Prints details about the user's Alpaca account, including account ID, balance, portfolio value, and buying power.
    
    Args:
        client (TradingClient): The Alpaca TradingClient object.
    """
    
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

def average_symbol_value(symbol:str,days:int)->float:
    """
    Retrieves the last `n` days of historical data for a given cryptocurrency symbol and returns the average
    closing price for that period.

    Args:
        symbol (str): The symbol of the cryptocurrency to retrieve data for, e.g. 'BTC/USD'.
        days (int): The number of days you want the average price for.

    Returns:
        float: The average closing price for the last 30 days of historical data for the specified cryptocurrency.
    """

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


def balance_check(client,spend):
    account = client.get_account()
    bal = account.cash
    available = bal - spend
    if available >= 0:
        return True
    else:
        return False


def DCA_logic(symbol,days,spend):
    symbol = 'BTC/USD'
    market_price = coin_price(symbol)
    average_price = average_symbol_value(symbol,days)
    not_bought_in = True
    not_bought_out = True
    #buy in first(only when market price is 5 percent less than avg price)
    while not_bought_in:
        market_price = coin_price(symbol)
        percent =((market_price - average_price)/average_price)*100
        if market_price >= average_price:
            sleep(300)
        elif  percent <= -5:
            # Only buy if the market price is at least 5% less than the average price
            _,qty = buy_price(client,symbol,spend)
            buy_in_price = market_price
            not_bought_in = False
        else:
            # Wait for some time before checking again
            sleep(300)
    #now need to buy out for profit
    while not_bought_out:
        market_price = coin_price(symbol)
        percent =((market_price - buy_in_price)/buy_in_price)*100
        if buy_in_price > market_price and percent >= 10:
            sell_marketprice(client,symbol,qty)

        


    

 




key ='PKMS1S5M1C60839ET2QC' 
skey='YaXCd0ItTQUPwFwPcRECyQs71UnuPlqnHhPZFjWR'

#signup()


client = TradingClient(key,skey)
_,qty= buy_price(client,'BTC/USD',20230.80)

pprint(qty)