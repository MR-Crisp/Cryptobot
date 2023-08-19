import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt


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



    def calcPoints(self):
        start = dt.datetime(2019,6,1)
        end = dt.datetime.now()
        df = pdr.get_data_yahoo(self.symbol, start, end) # creates dataframe of the symbol
        df['High'].plot(label = "High")
        pivots = []
        dates = [] #may or may not use dates as then it becomes complicated
        counter = 0
        lastPivot = 0
        Range = [0,0,0,0,0,0,0,0,0,0]
        dateRange = [0,0,0,0,0,0,0,0,0,0]


        #raw pivotpoints and dates
        for i in df.index:
            currentMax = max(Range,default=0)
            value = round(df['High'][i],2)
            Range = Range[1:9]
            Range.append(value)
            dateRange = dateRange[1:9]
            dateRange.append(i)

            if currentMax == max(Range,default=0):
                counter+=1
            else:
                counter=0
            if counter ==5:
                lastPivot = currentMax
                dateloc = Range.index(lastPivot)
                lastDate = dateRange[dateloc]
                pivots.append(lastPivot)
                dates.append(lastDate)
        



        #condensing pivots and flitering out similar and not needed points
        pivots = self.merge_list(pivots,12 ) #----------------------------------------------------------------note the threshold value for this is veryimportant for figuring out the sensitivity for the points
        print(str(pivots))

        #visulistaion of data to check the validity of the pivot points
        
        for index in range(len(pivots)):
            #plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],pivots[index]],linestyle = "-",linewidth = 2,marker = ",")
            plt.axhline(y = pivots[index], color = 'r', linestyle = '-')

        plt.show()



    def merge_list(self,a, thresh):
        # Get an array with indices off input array, such that each index
        # represent start of a group of close proximity elements
        i = np.flatnonzero(np.r_[True,np.diff(a)>thresh,True])

        # Sum based on those indices. Hence, each group is summed.
        sums = np.add.reduceat(a,i[:-1])

        # Get counts of each group
        counts = np.diff(i)

        # Get average of each group and round those for final o/p
        return np.round(sums/counts.astype(float))






bot = PivotPoints()

bot.calcPoints()