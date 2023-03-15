import BotFunctions as bot
from Crypto.Cipher import AES  # this is acting very wierd might have to replace
from getpass import getpass
from time import sleep
from alpaca.trading.client import TradingClient
from alpaca.data.requests import CryptoLatestQuoteRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest


# these 4 imports are used to figure out the DCA of a symbol:
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

# For pretty printing
from pprint import pprint

BTC = "BTC/USD"
ETH = "ETH/USD"

key = 'PKMS1S5M1C60839ET2QC'
skey = 'YaXCd0ItTQUPwFwPcRECyQs71UnuPlqnHhPZFjWR'

client = TradingClient(key, skey)


def simulation(startDate, endDate, client, symbol):
    bal = bot.balance_get(client)
    startDate = startDate.split("/")
    Syear = int(startDate[0])
    Smonth = int(startDate[1])
    Sday = int(startDate[2])

    endDate = endDate.split("/")
    Eyear = int(endDate[0])
    Emonth = int(endDate[1])
    Eday = int(endDate[2])
    # no keys required for crypto data
    crypto_client = CryptoHistoricalDataClient()

    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=datetime(Syear, Smonth, Sday),
        end=datetime(Eyear, Emonth, Eday)
    )

    bars = crypto_client.get_crypto_bars(request_params)
    bars = [bar._make(b) for b in bars]

    for bar in bars:
        open_price = bar.o
        close_price = bar.c
        pprint(close_price)

simulation("2022/9/1", "2022/11/1", client, BTC)
