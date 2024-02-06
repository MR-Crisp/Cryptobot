# https://aroussi.com/post/python-yahoo-finance
# USE ROLLING MEAN https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/


from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tools import *


class MyGUI(QMainWindow):
    def __init__(self):
        # loads the xml file
        super(MyGUI, self).__init__()
        #uic.loadUi("/Users/aamir/programming/crypto/gui.ui", self)
        uic.loadUi("./gui.ui",self)
        self.show()

        # configs the date note: this is slighty inefficient but works
        self.StartDate_tab1 = self.findChild(QDateEdit, "StartDate")

        self.EndDate_tab1 = self.findChild(QDateEdit, "EndDate")

        self.startdate_tab1 = str(
            self.Dateformat(self.StartDate_tab1.date())
        )  # convert to regular
        self.enddate_tab1 = str(
            self.Dateformat(self.EndDate_tab1.date())
        )  # convert to regular

        self.StartDate_tab1.dateChanged.connect(self.DateChanged)
        self.EndDate_tab1.dateChanged.connect(self.DateChanged)

        self.Stock_select_tab1 = self.findChild(QComboBox, "StockcomboBox")

        # does all of the slider configs
        self.CapitalSlider_tab1 = self.findChild(QSlider, "horizontalSlider")
        self.CapitalLabel_tab1 = self.findChild(QLabel, "CapitalLabel")
        self.CapitalSlider_tab1.setMinimum(1)
        self.CapitalSlider_tab1.setMaximum(10_000)
        self.CapitalSlider_tab1.setSingleStep(100)

        # graph configs ---------------------------------------------------------------- need to be worked out

        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)

        self.CapitalSlider_tab1.valueChanged.connect(self.calcCapitalSlider)

        # code for when button is pressed
        self.pushButton_tab1 = self.findChild(QPushButton, "pushButton_tab1")
        self.pushButton_tab1.clicked.connect(lambda: self.MainButtonClick())

        # code for the second tab

        self.StartDate_tab2 = self.findChild(QCalendarWidget, "tab2_StartDate")
        self.EndDate_tab2 = self.findChild(QCalendarWidget, "tab2_endDate")
        self.CapitalLabel_tab2 = self.findChild(QLabel, "tab2_capitalLabel")
        self.CapitalSlider_tab2 = self.findChild(QLabel, "tab2_capitalSlider")
        self.RiskLevelLabel_tab2 = self.findChild(QLabel,"tab2_risklevelLabel")
        self.RiskLevelSlider_tab2 = self.findChild(QLabel,"tab2_riskSlider")
        self.DropDownbox_tab2 = self.findChild(QComboBox,"tab2_dropDownBox")
        self.PushButtonMain_tab2 = self.findChild(QPushButton,"tab2_pushbuttonMain")
        self.CheckBonx_tab2 = self.findChild(QCheckBox,"tab2_checkBox")
        


    def calcCapitalSlider_tab2(self):
            self.value_tab2 = self.CapitalSlider_tab2.value()
            self.CapitalLabel_tab2.setText(str(self.value_tab2))

    def MainButton_tab2(self):
        bot = PivotPoints(self.DropDownbox_tab2.currentText(),self.StartDate_tab2,self.EndDate_tab2,self.RiskLevelLabel_tab2,36,self.value_tab2,0.95,1.1)
        bot.calcPoints()
        bot.pivot_logic()




    def calcCapitalSlider(self):
        value_tab1 = self.CapitalSlider_tab1.value()
        self.CapitalLabel_tab1.setText(str(value_tab1))
    
    

    def Dateformat(self, unformatted):
        day = str(unformatted.day())
        month = str(unformatted.month())
        year = str(unformatted.year())
        formatted = year + "-" + month + "-" + day
        return formatted

    def MainButtonClick(self):
        bot = averageCrossover(
            self.Stock_select_tab1.currentText(),
            self.startdate_tab1,
            self.enddate_tab1,
            4,
            20,
        )
        # bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
        bot.calc_MA()
        bot.algo(float(self.CapitalSlider_tab1.value()))
        self.OutputLabel_tab1 = self.findChild(QLabel, "OutputLabel")
        self.OutputLabel_tab1.setText(str(bot.profit))

    def DateChanged(self):
        self.startdate_tab1 = str(
            self.Dateformat(self.StartDate_tab1.date())
        )  # convert to regular
        self.enddate_tab1 = str(
            self.Dateformat(self.EndDate_tab1.date())
        )  # convert to regular

   




def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()


# bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
