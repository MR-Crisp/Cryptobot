#https://aroussi.com/post/python-yahoo-finance
#USE ROLLING MEAN https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic 




class averageCrossover:
    def __init__(self, symbol, startDate,endDate,shortWindow,longWindow):
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.__data = yf.Ticker(symbol).history(start=self.startDate, end=self.endDate)#private
        self.shortWindow = shortWindow
        self.longWindow = longWindow
        self.__FMA = ''
        self.__SMA = ''
        self.dateformat = '%Y-%m-%d'
        self.capital = 0 
        self.profit = 0 
        self.amount = 0


    
    def calc_MA(self):
        
        close = pd.DataFrame(self.__data.Close)

        
        self.__FMA = close.rolling(self.shortWindow).mean()
        self.__SMA = close.rolling(self.longWindow).mean()

    def algo(self,capital):
        close = pd.DataFrame(self.__data.Close)
        
        #clac the days between the two dates
        d1 = datetime.strptime(self.startDate,self.dateformat)
        d2 = datetime.strptime(self.endDate,self.dateformat)
        days = ((d2-d1).days)
        
        #start the simulation

        self.capital = capital
        bought = False
        

        
        for i in range(self.longWindow,int(len(self.__FMA))):
            #start the initial check of wheather the FMA is higher than the SMA and nothing has been bought yet

            if float(self.__FMA.iloc[i]) > float(self.__SMA.iloc[i]) and bought == False:
                #buy as many shares as possible 
                price = float(close.iloc[i])
                self.amount = int(self.capital/price)
                self.capital -=(self.amount*price)
                bought = True
            
            #now do sell check if the FMA is lower than the SMA AND BOUGHT IS TRUE

            elif float(self.__FMA.iloc[i]) < float(self.__SMA.iloc[i]) and bought == True:
                #sell all the shares and then add it to the capital
                price = float(close.iloc[i])
                self.capital += price*self.amount
                bought = False
                self.amount = 0
                print('sold')

        print(self.capital - capital)
        print(self.capital )

            # self.__SMA.iloc[i]        
        



class MyGUI(QMainWindow):
    def __init__(self):
        bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
        bot.calc_MA()
        super(MyGUI, self).__init__()
        uic.loadUi("C:/Users/akaam/Documents/Coding/Projects/Crypto bot/gui.ui",self)
        self.show()
        self.pushButton.clicked.connect(lambda: bot.algo(int(self.lineEdit.text())))
    











def main():
    

    
    
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()









