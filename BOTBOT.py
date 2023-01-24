
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame , TimeFrameUnit
import time
from alpaca_trade_api.common import URL
from alpaca_trade_api.stream import Stream

def auth():
    confirm = int(input('1 For new profile \n2 For existing profile \nenter here:   '))
    if confirm == 1:
        veri = False
        while not veri:
            key = input('Enter your public Key here :')
            sec_key = input('Enter your secret Key here :')
            try:
                api = tradeapi.REST(
                    key_id= key,
                    secret_key=sec_key,
                    base_url='https://paper-api.alpaca.markets'
                )
                account = api.get_account()
                if account.status == 'ACTIVE':
                    veri = True
                    print('verified')
            except:
                print('Error your Key or Secret Key are wrong')


api = tradeapi.REST(
    key_id='PKUW7TOSXWHBPGEVQC53',
    secret_key='T5gSy27X9Ov8AfsAp65ieDNn5Y5smDrmZVKSZpex',
    base_url='https://paper-api.alpaca.markets'
)


def trade_money(tradetype):
    order = api.submit_order(
        symbol='BTC/USD',
        qty=3,
        type='market',
        side=tradetype,
        
        time_in_force='ioc',) #has to be immediate or killed (ioc), so that the order either happens or it doesnt





#auth()




async def trade_call(t):
    print('trade', t)


async def quote_call(q):
    print('quote', q)


# Live stream of quotes and trades
stream = Stream(key_id='PKUW7TOSXWHBPGEVQC53',
                secret_key='T5gSy27X9Ov8AfsAp65ieDNn5Y5smDrmZVKSZpex',
                base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='iex',)  

# starting the feed
stream.subscribe_trades(trade_call, 'AAPL')
stream.subscribe_quotes(quote_call, 'IBM')

stream.run()

#redundant

