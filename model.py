#https://aroussi.com/post/python-yahoo-finance
#USE ROLLING MEAN https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/


from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from tools import *

class MyGUI(QMainWindow):
    def __init__(self):
        

        #loads the xml file
        super(MyGUI, self).__init__()
        uic.loadUi("C:/Users/akaam/Documents/Coding/Projects/Crypto bot/gui.ui",self)
        self.show()

        # configs the date note: this is slighty inefficient but works
        self.StartDate = self.findChild(QDateEdit, "StartDate")
        
        self.EndDate = self.findChild(QDateEdit, "EndDate")
        
        self.startdate  = str(self.Dateformat(self.StartDate.date())) # convert to regular
        self.enddate = str(self.Dateformat(self.EndDate.date())) # convert to regular

        
        self.StartDate.dateChanged.connect(self.DateChanged)
        self.EndDate.dateChanged.connect(self.DateChanged)

        # does all of the slider configs
        self.CapitalSlider = self.findChild(QSlider,"horizontalSlider")
        self.CapitalLabel = self.findChild(QLabel,"CapitalLabel")
        self.CapitalSlider.setMinimum(1)
        self.CapitalSlider.setMaximum(10_000)
        self.CapitalSlider.setSingleStep(100)

        #graph configs ---------------------------------------------------------------- need to be worked out
        



        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)

        self.CapitalSlider.valueChanged.connect(self.calcCapitalSlider)

        #code for when button is pressed
        self.pushButton.clicked.connect(lambda: self.MainButtonClick())
        
        
        

    def calcCapitalSlider(self):
        value  = self.CapitalSlider.value()
        self.CapitalLabel.setText(str(value))


    def Dateformat(self,unformatted):
        day = str(unformatted.day())
        month = str(unformatted.month())
        year = str(unformatted.year())
        formatted = year+"-"+month+"-"+day
        return formatted

    def MainButtonClick(self):
        bot =  averageCrossover("AAPL",self.startdate,self.enddate,4,20)
        #bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
        bot.calc_MA()
        bot.algo(float(self.CapitalSlider.value()))
        self.OutputLabel = self.findChild(QLabel,"OutputLabel")
        self.OutputLabel.setText(str(bot.profit))
        
    def DateChanged(self):
        self.startdate  = str(self.Dateformat(self.StartDate.date())) # convert to regular
        self.enddate = str(self.Dateformat(self.EndDate.date())) # convert to regular

        


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

    

if __name__ == '__main__':
     main()









#bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
