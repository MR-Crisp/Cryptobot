import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from itertools import islice
from dateutil.relativedelta import relativedelta


class averageCrossover:
    def __init__(self, symbol, startDate, endDate, shortWindow, longWindow):
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.data = yf.Ticker(symbol).history(start=self.startDate, end=self.endDate)
        self.shortWindow = shortWindow
        self.longWindow = longWindow
        self.__FMA = None
        self.__SMA = None
        self.dateformat = '%Y-%m-%d'
        self.capital = 0
        self.profit = 0
        self.amount = 0
    
    def calc_MA(self):
        close = pd.DataFrame(self.data.Close, columns=['Close'])
        self.__FMA = close.rolling(self.shortWindow).mean()
        self.__SMA = close.rolling(self.longWindow).mean()
    
    def algo(self, capital):
        close = pd.DataFrame(self.data.Close)

        self.capital = capital
        bought = False
        sell_comparison = self.__FMA.values < self.__SMA.values
        sell_comparison_str = np.where(sell_comparison, 'True', 'False')
        self.__FMA['sell_comparison'] = sell_comparison_str

        for i in range(self.longWindow, len(self.__FMA)):
            if (self.__FMA.iloc[i]['sell_comparison'] == 'False') and (not bought):
                price = close.iloc[i].astype(float)
                self.amount = int(self.capital / price)
                self.capital -= self.amount * price
                bought = True
                
            elif (self.__FMA.iloc[i]['sell_comparison'] == 'True') and bought:
                price = close.iloc[i].astype(float)
                self.capital += price.iloc[0] * self.amount
                bought = False
                self.amount = 0
                

        self.profit = float(self.capital - capital)

# Create an instance of the class and run the strategy
#bot = averageCrossover('AAPL', "2017-01-01", "2017-09-30", 4, 20)


#https://www.youtube.com/watch?v=Gdpaita5GcE link for calc pivot points


class PivotPoints:

    def visualize_pivots(self):
        ax = self.df['Close'].plot(label='Close')
        for pivot in self.pivots:
            if pivot >= self.df['Close'].min() and pivot <= self.df['Close'].max():
                plt.axhline(y=pivot, color='r', linestyle='--', label='Pivot')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Close Prices and Pivot Points')
        plt.legend()
        plt.show()


    def __init__(self,start,end,thresh,period,capital,sl,tp):
        self.symbol = 'AAPL'
        yf.pdr_override() # activatees the yahoo workarounds
        self.start = start
        self.end = end
        self.df = pdr.get_data_yahoo(self.symbol, self.start- relativedelta(months=period), self.start) # creates dataframe of the symbol
        self.pivots = []
        self.threshold = thresh # ------------------------------------------------------------------------- very important parameter, as it is used to clean the data
        self.capital = capital 
        self.amount = 0
        self.sl = sl  #----------------------------------------------------------------
        self.tp = tp#----------------------------------------------------------------
        self.buy_in = 0
        self.current_price = 0
      
    def merge_list(self, a, thresh):
        merged = []
        for value in a:
            if len(merged) == 0 or abs(value - merged[-1]) > thresh:
                merged.append(value)
        return merged




    def calcPoints(self):
        
        self.pivots = []

        for i in range(4, len(self.df) - 1):
            recent_low_prices = self.df['Low'][i-4:i+1]
            recent_high_prices = self.df['High'][i-4:i+1]
            currentMin = min(recent_low_prices)
            currentMax = max(recent_high_prices)
            
            if currentMin == self.df['Low'][i] or currentMax == self.df['High'][i]:
                self.pivots.append(self.df['Close'][i])
        self.pivots = self.merge_list(self.pivots, self.threshold)
        




    def pivot_logic(self):
        self.df = pdr.get_data_yahoo(self.symbol, self.start, self.end) # inits new df with the new relevant dates
        init_price = self.df['Close'].iloc[0]   # gets the first line of the df

        bought = False # set the bought variable so that the for loop can be broken later

        for index, row in self.df.iloc[1:].iterrows():   # starts iterating through the df starting from SECOND row (least complex way to do this)
            self.current_price = row['Close']
            if not bought and init_price < self.current_price: # only allows for buy logic to run if the price is going up (compares current price and 1 price before it)
                buy_condition = self.compare_pivots(init_price, self.current_price, self.pivots)
                if buy_condition:
                    self.amount = int(self.capital / self.current_price)
                    self.capital -= self.amount * self.current_price
                    bought = True
                    self.buy_in = self.current_price 



            # take profit/stop loss logic
            if bought:
                percent = 1 + self.percent_change(self.buy_in, self.current_price) # we want the percentage, not the change used to calculate when the TP/SL should activate

                if percent > self.tp: # take profit
                    self.capital += self.current_price * self.amount
                    bought = False
                    self.amount = 0

                elif percent < self.sl: # stop loss logic
                    self.capital += self.current_price * self.amount
                    bought = False
                    self.amount = 0
            init_price = self.current_price

        self.capital += self.current_price * self.amount
        print("Final capital:", self.capital)





                
    def compare_pivots(self, init, current, pivot_list): # compares the WHOLE list to the two prices
        for item in pivot_list: 
            if init < item < current:  
                return True
        return False

    def percent_change(self,start_point, end_point):
        # This is going to be a little long but bare with me here
        return ((float(end_point) - start_point) / abs(start_point)) 


# bot = PivotPoints(dt.datetime(2017,1,1),dt.datetime(2023,6,1),2,36,1000,0.95,1.1)
# bot.calcPoints()
# bot.pivot_logic()

#bot.visualize_pivots()