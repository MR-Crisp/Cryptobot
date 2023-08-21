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

    def __init__(self):
        self.symbol = 'AAPL'
        yf.pdr_override() # activatees the yahoo workarounds
        self.start = dt.datetime(2020,6,1)
        self.end = dt.datetime.now() - relativedelta(months=6)
        self.now = dt.datetime.now()
        self.df = pdr.get_data_yahoo(self.symbol, self.start, self.end) # creates dataframe of the symbol
        #self.df['High'].plot(label = "High")
        self.pivots = []
        self.dates = [] #may or may not use dates as then it becomes complicated
        self.counter = 0
        self.threshold = 1 # ------------------------------------------------------------------------- very important parameter, as it is used to clean the data
        self.capital = 1000
        self.amount = 0
        self.sl = 0.95 #----------------------------------------------------------------
        self.tp = 1.1#----------------------------------------------------------------
        self.buyin = 0
        self.current_price = 0


    def calcPoints(self):
        lastPivot = 0
        Range = [0,0,0,0,0,0,0,0,0,0]
        dateRange = [0,0,0,0,0,0,0,0,0,0]
        #raw pivotpoints and dates
        for i in self.df.index:
            currentMax = max(Range,default=0)
            value = round(self.df['High'][i],2)
            Range = Range[1:9]
            Range.append(value)
            dateRange = dateRange[1:9]
            dateRange.append(i)

            if currentMax == max(Range,default=0):
                self.counter+=1
            else:
                self.counter=0
            if self.counter ==5:
                lastPivot = currentMax
                dateloc = Range.index(lastPivot)
                lastDate = dateRange[dateloc]
                self.pivots.append(lastPivot)
                self.dates.append(lastDate)
        



        #condensing pivots and flitering out similar and not needed points
        self.pivots = self.merge_list(self.pivots,self.threshold ) #----------------------------------------------------------------note the threshold value for this is veryimportant for figuring out the sensitivity for the points


        # #visulistaion of data to check the validity of the pivot points
        
        # for index in range(len(self.pivots)):
        #     #plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],pivots[index]],linestyle = "-",linewidth = 2,marker = ",")
        #     plt.axhline(y = self.pivots[index], color = 'r', linestyle = '-')

        # plt.show()



    def merge_list(self,a, thresh): # cleans the pivot points (merges close numbers together using vectorisation)
        i = np.flatnonzero(np.r_[True,np.diff(a)>thresh,True])
        sums = np.add.reduceat(a,i[:-1])
        counts = np.diff(i)
        return np.round(sums/counts.astype(float))


    def pivot_logic(self):
        

        self.simStart = self.now - relativedelta(months=6)        
        

        self.df = pdr.get_data_yahoo(self.symbol, self.simStart, self.now) # inits new df with the new  relevant dates


        init_price = self.df['Close'].iloc[0]   # gets the first line of the df

        bought = False # set the bought variable so that the for loop can be broken later

        for index, row in self.df.iloc[1:].iterrows():   # starts iterating through the df starting from SECOND row (least complex way to do this)
            self.current_price = row['Close']
            if init_price < self.current_price and bought == False: # only allows for buy logic to run if the price is going up (compares current price and 1 price before it)
                if self.compare_pivots(init_price,self.current_price,self.pivots):  # compares pivots to the two prices, to see if a point is in between them
                    self.amount = int(self.capital / self.current_price)
                    self.capital -= self.amount * self.current_price
                    bought = True
                    self.buyin = self.current_price 
            
            
            #take profit/ stop loss logic
            if bought:
                percent = 1 + self.percent_change(self.buyin,self.current_price) # we wamt the percentage, not the change used to calcuate when the TP/SL should activate

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
        print(self.capital)






            
    def compare_pivots(self,init,current,pivot_list): # compares the WHOLE list to the two prices
        for item in pivot_list:
            if init < item < current:
                return True
        return False

    def percent_change(self,start_point, end_point):
        # This is going to be a little long but bare with me here
        return ((float(end_point) - start_point) / abs(start_point)) 


bot = PivotPoints()
bot.calcPoints()
bot.pivot_logic()

