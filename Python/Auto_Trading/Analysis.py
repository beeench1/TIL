import sys
import matplotlib
matplotlib.use('Qt4Agg')
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Kiwoom1 import *
from concurrent.futures import ProcessPoolExecutor
import functools
import numpy as np
import threading
from matplotlib import style
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt

form_class=uic.loadUiType("an.ui")[0]

class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom=Kiwoom1()
        self.kiwoom.CommConnect()

                    # Currency
        self.Market={"AUD" : "6A000",
                    "POUND" : "6B000",
                    "CAD" : "6C000",
                    "EURO" : "6E000",
                    "YEN" : "6J000",
                    "FRANC" : "6S000",

                    # Index
                    "S&P" : "ES000",
                    "CNY" : "CN000",

                    # Bond
                    "10T" : "ZN000",

                    # Commodity
                    "GOLD" : "GC000",
                    "COPPER" : "HG000",
                    "SILVER" : "SI000",
                    "OIL" : "CL000"}

        self.pushButton.clicked.connect(self.Corr)

    def Corr(self,*args):
        self.DatalistName=[]
        self.Datalist=[]

        # 데이터 불러오기
        for MarketName, MarketCode in  self.Market.items():
            self.kiwoom.SetInputValue("종목코드",MarketCode)
            self.kiwoom.SetInputValue("시간단위", "10")
            self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

            x = MarketName
            x_1 = str(x)

            # 데이터 프레임 만들기 및 수정
            Data = pd.DataFrame(self.kiwoom.minute,index=self.kiwoom.minute['date'],
                                columns=['Close', 'High', 'Low', 'Open', 'Volume'])
            Data1 = Data.sort_index(0,ascending=False)

            # 보조지표
            self.kiwoom.MA(Data1, 5, 100, 200, 600)
            self.kiwoom.Bolinger(Data1, 200, 2.5)
            self.kiwoom.MAX(Data1, 200)
            self.kiwoom.MIN(Data1, 200)

            self.Datalist.append(Data1)  # 시장 데이터
            self.DatalistName.append(x)  # 시장

        self.Datalen=len(self.DatalistName)
        self.DataSet={}
        for i in range(self.Datalen):
            self.DataSet[self.DatalistName[i]]=self.Datalist[i]['Close']

        DATASET = pd.DataFrame(self.DataSet)
        CORR = pd.DataFrame(DATASET.corr())

        plt.figure(figsize=(12,6))
        t=np.arange(1.0,600.0)

        plt.subplot(411)
        plt.plot(t,DATASET['AUD'])
        plt.grid()

        plt.subplot(412)
        plt.plot(t,DATASET['GOLD'])

        plt.subplot(413)
        plt.plot(t,DATASET['EURO'])
        plt.grid()

        plt.show()


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()