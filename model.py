# https://aroussi.com/post/python-yahoo-finance
# USE ROLLING MEAN https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/


from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tools import *
import datetime as dt


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

        self.ShortWindow_tab1 = self.findChild(QLineEdit,"ShortWindow_tab1")
        self.LongWindow_tab1 = self.findChild(QLineEdit,"LongWindow_tab1")

        self.CapitalSlider_tab1.valueChanged.connect(self.calcCapitalSlider)

        # code for when button is pressed
        self.pushButton_tab1 = self.findChild(QPushButton, "pushButton_tab1")
        self.pushButton_tab1.clicked.connect(lambda: self.MainpushButton_tab1())

        # code for the second tab

        self.StartDate_tab2 = self.findChild(QDateEdit, "StartDate_tab2")
        self.StartDate_tab2.dateChanged.connect(self.DateChanged_tab2)

       


        self.EndDate_tab2 = self.findChild(QDateEdit, "EndDate_tab2")
        self.EndDate_tab2.dateChanged.connect(self.DateChanged_tab2)

        self.CapitalLabel_tab2 = self.findChild(QLabel, "tab2_capitalLabel")
        self.CapitalSlider_tab2 = self.findChild(QSlider, "tab2_capitalSlider")
        self.RiskLevelLabel_tab2 = self.findChild(QLabel,"tab2_risklevelLabel")
        self.RiskLevelSlider_tab2 = self.findChild(QSlider,"tab2_riskSlider")
        self.DropDownbox_tab2 = self.findChild(QComboBox,"tab2_dropDownBox")
        self.PushButtonMain_tab2 = self.findChild(QPushButton,"tab2_pushbuttonMain")
        self.CheckBonx_tab2 = self.findChild(QCheckBox,"tab2_checkBox")
        self.StopLoss_tab2 = self.findChild(QLineEdit,"StopLoss_tab2")
        self.TakeProfit_tab2 = self.findChild(QLineEdit,"TakeProfit_tab2")

        self.CapitalSlider_tab2.setMinimum(1)
        self.CapitalSlider_tab2.setMaximum(10_000)
        self.CapitalSlider_tab2.setSingleStep(100)
        self.RiskLevelSlider_tab2.setMinimum(1)
        self.RiskLevelSlider_tab2.setMaximum(5)
        self.RiskLevelSlider_tab2.setSingleStep(1)

        self.RiskLevelSlider_tab2.valueChanged.connect(self.calcRiskSlider_tab2)
        self.CapitalSlider_tab2.valueChanged.connect(self.calcCapitalSlider_tab2)
        self.PushButtonMain_tab2.clicked.connect(lambda: self.MainpushButton_tab2())



    def calcRiskSlider_tab2(self):
        self.riskvalue_tab2 = self.RiskLevelSlider_tab2.value()
        self.RiskLevelLabel_tab2.setText(str(self.riskvalue_tab2))


    def calcCapitalSlider_tab2(self):
        self.value_tab2 = self.CapitalSlider_tab2.value()
        self.CapitalLabel_tab2.setText(str(self.value_tab2))
    
    def MainpushButton_tab2(self):
        some = PivotPoints(self.DropDownbox_tab2.currentText(),str(self.Dateformat(self.StartDate_tab2.date())),str(self.Dateformat(self.EndDate_tab2.date())),self.riskvalue_tab2,36,self.value_tab2,float(self.StopLoss_tab2.text()),float(self.TakeProfit_tab2.text()))
        some.calcPoints()
        some.pivot_logic()
        print("some")



    def calcCapitalSlider(self):
        value_tab1 = self.CapitalSlider_tab1.value()
        self.CapitalLabel_tab1.setText(str(value_tab1))

    

    def Dateformat(self, unformatted):
        day = str(unformatted.day())
        month = str(unformatted.month())
        year = str(unformatted.year())
        formatted = year + "-" + month + "-" + day
        print(formatted)
        return formatted
    


    def MainpushButton_tab1(self):
        bot = averageCrossover(
            self.Stock_select_tab1.currentText(),
            self.startdate_tab1,
            self.enddate_tab1,
            int(self.ShortWindow_tab1.text()),
            int(self.LongWindow_tab1.text()),
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

   
    def DateChanged_tab2(self):
        self.EndDate_tab2 = self.EndDate_tab2

        self.StartDate_tab2 =self.StartDate_tab2
        



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    print("hi")
    main()


# bot = averageCrossover('AAPL',"2017-01-01","2017-09-30",4,20)
