
import matplotlib
matplotlib.use('Qt4Agg')
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom1 import *
from concurrent.futures import ProcessPoolExecutor
import functools
import threading
from matplotlib import style
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt
import requests


form_class=uic.loadUiType("pytrader4.ui")[0]

class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom=Kiwoom1()
        self.kiwoom.CommConnect()

        self.Code = {"Gold": "GCQ18",
                     "Euro": "6EU18",
                     "Oil": "CLQ18",
                     "Pound": "6BH18",
                     "China" : "CNM18",
                     "Yen" : "6JU18",
                     "Franc" : "6SH18"}  # 주문코드

        self.pushButton.clicked.connect(self.timeout)
        self.pushButton_2.clicked.connect(self.Close)
        self.pushButton_3.clicked.connect(self.Corr)
        self.target_url='https://maker.ifttt.com/trigger/Trading/with/key/b_r1S3XmmB-2Wx-GrL5DWe'

    def timeout(self):

        # 시간
        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time
        self.listWidget_6.addItem("Started on" + "_" + self.time_msg)

        # 시스템 시작 전 초기 설정값
        '''
                Market : Gold, Euro, Oil, Yen
                Position : BBANDS_Long, BBANDS_Short, SS_Long, SS_Short, DLINE_Long, DLINE_Short
        '''

        self.Market = [self.comboBox.currentText(), 1]
        self.Position = [self.comboBox_2.currentText(), 1]
        self.bet_rate=self.doubleSpinBox.value()

        self.Holding = self.comboBox.currentText()
        self.exe()

    def exe(self):
        self.timer_0 = QTimer(self)
        self.timer_0.start(600000)  # 1000 = 1초


        '''
        BBANDS
        BB_TS
        SS
        DLINE
        Target_limit
        Long
        Short
        '''

        timerCallback2 = functools.partial(self.Target_limit, market="Yen")

        exe_2 = self.timer_0.timeout.connect(timerCallback2)

        exe = ProcessPoolExecutor(max_workers=5)
        exe.submit(exe_2)

    def Long(self, market):
        market_ = str(market)
        strategy_ = "ONLY_LONG"
        position_1 = "SHORT"
        position_2 = "LONG"
        position_0 = "CLEAR"

        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "Pound":
            self.DataCode = "6B000"
            self.OrderCode = self.Code["Pound"]
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
        elif market == "Franc":
            self.DataCode = "6S000"
            self.OrderCode = self.Code["Franc"]
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거급
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk = str(round(self.kiwoom.account[2], 2))

        if self.Margin > 0:
            self.po = 1
        else:
            self.po = 0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        # 가격 데이터 불러오기
        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)

        # 지표 생성
        self.kiwoom.MA(df1, 5, 200, 599)
        self.kiwoom.Bolinger(df1, 200, 2.5)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 200)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 200, 150, 6)  # R.-est
        self.kiwoom.BB_TS(df1, 200, 4, 200, 6)  # BB_TS

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c_1 = df1['Close'][1]
        c_2 = df1['Close'][2]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]
        o_1 = df1['Open'][1]
        o_2 = df1['Open'][2]
        v = df1['Volume'][0]
        v_1 = df1['Volume'][1]
        v_2 = df1['Volume'][2]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma599 = df1['MA599'][0]
        bbandsup = df1['BandsUp200_2.5'][0]
        bbandsdown = df1['BandsDown200_2.5'][0]
        va200 = df1['VA200'][0]
        atr200 = df1['ATR200'][0]
        atr1 = df1['ATR1'][0]
        atr1_1 = df1['ATR1'][1]
        atr1_2 = df1['ATR1'][2]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU6'][0]
        TD = df1['TD6'][0]
        BTU200 = df1['BTU'][0]
        BTD200 = df1['BTD'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1) < 1:
            self.Lots1 = int(1)
        else:
            self.Lots1 = int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1112")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2) < 1:
            self.Lots2 = int(1)
        else:
            self.Lots2 = int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # bbands
        if (c - bbandsup) * (c_1 - bbandsup) < 0 \
            and c > bbandsup \
            and c > o \
            and c > ma200 \
            and v >= va200 * 2 \
            and c >= highest200 \
            and atr1 >= atr200 * 4 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin == 0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1",
                                  "0")
            self.Market[0] = market
            self.Position[0] = "bbands_Long"
            self.listWidget.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Long" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + "_" + "Strategy : Bolinger Bands" + "_" + "Long" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        elif ma5<ma200 \
            and self.Position[0]=="bbands_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : Bolinger Bands"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : Bolinger Bands"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # SS
        elif c>o \
            and c_1>o_1 \
            and c_2>o_2 \
            and v>=va200*2 \
            and atr1>=atr200*2 \
            and v_1>=va200*2 \
            and atr1_1>=atr200*2 \
            and v_2>=va200*2 \
            and atr1_2>=atr200*2 \
            and ma5>ma200 \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="SS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : SS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : SS"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        elif ma5<ma200 \
            and self.Position[0]=="SS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : SS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : SS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})


        # BB_TS
        elif (c-BTD200)*(o-BTD200)<0 \
            and c>BTD200 \
            and c>o \
            and ma5<ma599 \
            and v>=va200*3 \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="BBTS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : BBTS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : BBTS"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        elif c<=lowest200 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c-self.doubleSpinBox_2.value())*(c_1-self.doubleSpinBox_2.value())<0 \
            and c<c_1 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_' + str(self.Margin) + '_' + 'LONG Processing' + '_' + self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_' + str(self.Margin) + '_' + 'LONG Processing' + '_' + self.time_msg)
            self.fw2.close()

    def Short(self, market):
        market_ = str(market)
        strategy_ = "ONLY_SHORT"
        position_1 = "SHORT"
        position_2 = "LONG"
        position_0 = "CLEAR"

        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "Pound":
            self.DataCode = "6B000"
            self.OrderCode = self.Code["Pound"]
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
        elif market == "Franc":
            self.DataCode = "6S000"
            self.OrderCode = self.Code["Franc"]
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거급
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk = str(round(self.kiwoom.account[2], 2))

        if self.Margin > 0:
            self.po = 1
        else:
            self.po = 0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        # 가격 데이터 불러오기
        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                              columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)

        # 지표 생성
        self.kiwoom.MA(df1, 5, 200, 599)
        self.kiwoom.Bolinger(df1, 200, 2.5)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 200)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 200, 150, 6)  # R.-est
        self.kiwoom.BB_TS(df1, 200, 4, 200, 6)  # BB_TS

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c_1 = df1['Close'][1]
        c_2 = df1['Close'][2]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]
        o_1 = df1['Open'][1]
        o_2 = df1['Open'][2]
        v = df1['Volume'][0]
        v_1 = df1['Volume'][1]
        v_2 = df1['Volume'][2]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma599 = df1['MA599'][0]
        bbandsup = df1['BandsUp200_2.5'][0]
        bbandsdown = df1['BandsDown200_2.5'][0]
        va200 = df1['VA200'][0]
        atr200 = df1['ATR200'][0]
        atr1 = df1['ATR1'][0]
        atr1_1 = df1['ATR1'][1]
        atr1_2 = df1['ATR1'][2]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU6'][0]
        TD = df1['TD6'][0]
        BTU200 = df1['BTU'][0]
        BTD200 = df1['BTD'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1) < 1:
            self.Lots1 = int(1)
        else:
            self.Lots1 = int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1112")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2) < 1:
            self.Lots2 = int(1)
        else:
            self.Lots2 = int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # bbands
        if (c - bbandsdown) * (c_1 - bbandsdown) < 0 \
            and c > bbandsdown \
            and c < o \
            and c < ma200 \
            and v >= va200 * 2 \
            and c <= lowest200 \
            and atr1 >= atr200 * 4 \
            and self.Position[0] == 'Nothing' \
            and self.Margin == 0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0",
                                      "1","0")
            self.Market[0] = market
            self.Position[0] = "bbands_Short"
            self.listWidget.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                    market + "_" + "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + "_" + "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        elif ma5 > ma200 \
            and self.Position[0] == "bbands_Short" \
            and self.Market[0] == market \
            and self.Margin > 0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0", "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                    market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                    market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(
                    market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # SS
        elif c < o \
            and c_1 < o_1 \
            and c_2 < o_2 \
            and v >= va200 * 2 \
            and atr1 >= atr200 * 2 \
            and v_1 >= va200 * 2 \
            and atr1_1 >= atr200 * 2 \
            and v_2 >= va200 * 2 \
            and atr1_2 >= atr200 * 2 \
            and ma5 < ma200 \
            and self.Position[0] == 'Nothing' \
            and self.Margin == 0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0",
                                      "1", "0")
            self.Market[0] = market
            self.Position[0] = "SS_Short"
            self.listWidget.addItem(market + "_" + "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + "_" + "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        elif ma5 > ma200 \
            and self.Position[0] == "SS_Short" \
            and self.Market[0] == market \
            and self.Margin > 0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0", "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                    market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                    market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})


        # BB_TS
        elif (c - BTU200) * (o - BTU200) < 0 \
            and c < BTU200 \
            and c < o \
            and ma5 > ma599 \
            and v >= va200 * 3 \
            and self.Position[0] == 'Nothing' \
            and self.Margin == 0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0",
                                      "1", "0")
            self.Market[0] = market
            self.Position[0] = "BBTS_Short"
            self.listWidget.addItem(market + "_" + "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + "_" + "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        elif c <= lowest200 \
            and self.Position[0] == "BBTS_Short" \
            and self.Market[0] == market \
            and self.Margin > 0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0", "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                    market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                    market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c - self.doubleSpinBox_2.value()) * (c_1 - self.doubleSpinBox_2.value()) < 0 \
            and c > c_1 \
            and self.Position[0] == "BBTS_Short" \
            and self.Market[0] == market \
            and self.Margin > 0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0","1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                    market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                    market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_' + str(self.Margin) + '_' + 'SHORT Processing' + '_' + self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_' + str(self.Margin) + '_' + 'SHORT Processing' + '_' + self.time_msg)
            self.fw2.close()

    # Trend : bbands
    def BBANDS(self,market):
        market_=str(market)
        strategy_="BBANDS"
        position_1="SELL"
        position_2="BUY"
        position_0="Clear"
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
            self.Tick = 100
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
            self.Tick = 125000
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
            self.Tick = 1000
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
            self.Tick = 12.5
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
            self.Tick = 10.0
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거금
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk=str(round(self.kiwoom.account[2],2))

        if self.Margin>0:
            self.po=1
        else:
            self.po=0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))  # 포지션 여부
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        # 가격 데이터 불러오기
        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.MA(df1, 5, 200, 400, 600)
        self.kiwoom.Bolinger(df1, 400, 2.5)
        self.kiwoom.VA(df1, 400)
        self.kiwoom.ATR(df1, 400)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1,200)
        self.kiwoom.MIN(df1,200)
        self.kiwoom.MAX(df1, 400)
        self.kiwoom.MIN(df1, 400)

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c1 = df1['Close'][1]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma600 = df1['MA600'][0]
        bbandsup = df1['BandsUp400_2.5'][0]
        bbandsdown = df1['BandsDown400_2.5'][0]
        va400 = df1['VA400'][0]
        atr400 = df1['ATR400'][0]
        atr1 = df1['ATR1'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        highest400 = df1['highest400'][0]
        lowest400 = df1['lowest400'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1)<1:
            self.Lots1=int(1)
        else:
            self.Lots1=int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1112")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2)<1:
            self.Lots2=int(1)
        else:
            self.Lots2=int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # Risk
        self.Risk_Long1 = round((ma200-c)*self.Tick,2)
        self.Risk_Long2 = round((lowest200-c)*self.Tick,2)
        self.Risk_Short1 = round((c-ma200)*self.Tick,2)
        self.Risk_Short2 = round((c-highest200)*self.Tick,2)

        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(str(self.Risk_Long1)))
        self.tableWidget_2.setItem(1, 0, QTableWidgetItem(str(self.Risk_Long2)))
        self.tableWidget_2.setItem(2, 0, QTableWidgetItem(str(self.Risk_Short1)))
        self.tableWidget_2.setItem(3, 0, QTableWidgetItem(str(self.Risk_Short2)))

        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(self.Risk_Long1*self.Lots2)))
        self.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(self.Risk_Long2*self.Lots2)))
        self.tableWidget_2.setItem(2, 1, QTableWidgetItem(str(self.Risk_Short1*self.Lots2)))
        self.tableWidget_2.setItem(3, 1, QTableWidgetItem(str(self.Risk_Short2*self.Lots2)))


        # bbands 전략 조건식
        # 매수
        if (c-bbandsup)*(c1-bbandsup)<0 \
            and c>bbandsup \
            and c>o \
            and ma5>ma200 \
            and v>=va400*2.5 \
            and c>=highest400 \
            and atr1>=atr400 \
            and self.comboBox_3.currentText()=="ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin == 0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="BBANDS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : Bolinger Bands"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Long" + "_" + self.time_msg)


            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        # 매도
        elif (c-bbandsdown)*(c1-bbandsdown)<0 \
            and c<bbandsdown \
            and c<o \
            and ma5<ma200 \
            and v>=va400*2.5 \
            and c<=lowest400 \
            and atr1>=atr400 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "BBANDS_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)

            r2 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "BBANDS_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "5057928272", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "BBANDS_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매수 청산
        elif ma5<ma200 \
            and self.Position[0]=="BBANDS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : Bolinger Bands"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="BBANDS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # 매도 청산
        elif ma5>ma200 \
            and self.Position[0]=="BBANDS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : Bolinger Bands"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="BBANDS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req1", "1101", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'BBANDS Processing'+'_'+ self.time_msg)

    # Reversal : Bolinger Bands Trailing Stop
    def BB_TS(self,market):
        market_ = str(market)
        strategy_ = "BB_TS"
        position_1 = "SELL"
        position_2 = "BUY"
        position_0 = "Clear"
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "Pound":
            self.DataCode = "6B000"
            self.OrderCode = self.Code["Pound"]
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
        elif market == "Franc":
            self.DataCode = "6S000"
            self.OrderCode = self.Code["Franc"]
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거금
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk=str(round(self.kiwoom.account[2],2))

        if self.Margin>0:
            self.po=1
        else:
            self.po=0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))  # 포지션 여부
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        # 데이터 불러오기
        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.MA(df1, 5, 200, 400, 600)
        self.kiwoom.Bolinger(df1, 200, 3)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 200)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 600, 100, 5)
        self.kiwoom.V_est(df1,200)
        self.kiwoom.BB_TS(df1, 200, 4, 200, 6)

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c1 = df1['Close'][1]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma600 = df1['MA600'][0]
        bbandsup = df1['BandsUp200_3'][0]
        bbandsdown = df1['BandsDown200_3'][0]
        va200 = df1['VA200'][0]
        atr200 = df1['ATR200'][0]
        atr1 = df1['ATR1'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU5'][0]
        TD = df1['TD5'][0]
        Highest_volume=df1['V_est200'][0]
        BTU200= df1['BTU'][0]
        BTD200 = df1['BTD'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1)<1:
            self.Lots1=int(1)
        else:
            self.Lots1=int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2)<int(1):
            self.Lots2=int(1)
        else:
            self.Lots2=int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # BB_TS 전략 조건식
        # 매수
        if (c-BTD200)*(o-BTD200)<0 \
            and c>BTD200 \
            and c>o \
            and ma5<ma600 \
            and v>=va200*2 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="BBTS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : BBTS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Long" + "_" + self.time_msg)

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        # 매도
        elif (c-BTU200)*(o-BTU200)<0 \
            and c<BTU200 \
            and c<o \
            and ma5>ma600 \
            and v>=va200*2 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "BBTS_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)

            r2 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "BBTS_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "BBTS_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매수 청산
        elif c<=lowest200 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c-ma600)*(c1-ma600)<0 \
            and c<c1 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c-self.doubleSpinBox_2.value())*(c1-self.doubleSpinBox_2.value())<0 \
            and c<c1 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # 매도 청산
        elif c>=highest200 \
            and self.Position[0]=="BBTS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r5 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c-ma600)*(c1-ma600)<0 \
            and c>c1 \
            and self.Position[0]=="BBTS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r6 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (c-self.doubleSpinBox_2.value())*(c1-self.doubleSpinBox_2.value())<0 \
            and c>c1 \
            and self.Position[0]=="BBTS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req2", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r6 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'BBTS Processing'+'_'+ self.time_msg)

    # Reversal : DLINE
    def DLINE(self,market):
        market_ = str(market)
        strategy_ = "DLINE"
        position_1 = "SELL"
        position_2 = "BUY"
        position_0 = "Clear"
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
            self.Tick = 100
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
            self.Tick = 125000
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
            self.Tick = 1000
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
            self.Tick = 12.5
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
            self.Tick = 10.0
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거금
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk=str(round(self.kiwoom.account[2],2))

        if self.Margin>0:
            self.po=1
        else:
            self.po=0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))  # 포지션 여부
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.MA(df1, 5, 200, 400, 600)
        self.kiwoom.Bolinger(df1, 200, 3)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 200)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.MAX(df1, 600)
        self.kiwoom.MIN(df1, 600)
        self.kiwoom.TrailingStop(df1, 200, 150, 6)
        self.kiwoom.V_est(df1,200)
        self.kiwoom.BB_TS(df1, 200, 4, 200, 6)
        self.kiwoom.DLine(df1, 200, 400, 1)

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c1 = df1['Close'][1]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma600 = df1['MA600'][0]
        bbandsup = df1['BandsUp200_3'][0]
        bbandsdown = df1['BandsDown200_3'][0]
        va200 = df1['VA200'][0]
        atr200 = df1['ATR200'][0]
        atr1 = df1['ATR1'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        lowest600 = df1['lowest600'][0]
        highest600 = df1['highest600'][0]
        Dis = df1['Disparity'][0]
        Dis_1 = df1['Disparity'][1]
        DLine = df1['DLine'][0]

        TU6 = df1['TU6'][0]
        TD6 = df1['TD6'][0]
        Highest_volume=df1['V_est200'][0]
        BTU200= df1['BTU']
        BTD200 = df1['BTD']

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1)<1:
            self.Lots1=int(1)
        else:
            self.Lots1=int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2)<1:
            self.Lots2=int(1)
        else:
            self.Lots2=int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # Risk
        self.Risk_Long1 = round((ma200 - c) * self.Tick, 2)
        self.Risk_Long2 = round((lowest200 - c) * self.Tick, 2)
        self.Risk_Short1 = round((c - ma200) * self.Tick, 2)
        self.Risk_Short2 = round((c - highest200) * self.Tick, 2)

        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(str(self.Risk_Long1)))
        self.tableWidget_2.setItem(1, 0, QTableWidgetItem(str(self.Risk_Long2)))
        self.tableWidget_2.setItem(2, 0, QTableWidgetItem(str(self.Risk_Short1)))
        self.tableWidget_2.setItem(3, 0, QTableWidgetItem(str(self.Risk_Short2)))

        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(self.Risk_Long1 * self.Lots2)))
        self.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(self.Risk_Long2 * self.Lots2)))
        self.tableWidget_2.setItem(2, 1, QTableWidgetItem(str(self.Risk_Short1 * self.Lots2)))
        self.tableWidget_2.setItem(3, 1, QTableWidgetItem(str(self.Risk_Short2 * self.Lots2)))

        # DLINE 전략 조건식
        # 매수
        if (Dis_1-DLine)*(Dis-DLine)<0 \
            and c>c1 \
            and Dis_1>Dis \
            and ma5<ma600 \
            and atr1>atr200*1 \
            and v>=va200*2 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="DLINE_Long"
            self.listWidget.addItem(market+"_"+"Strategy : DLINE"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : DLINE" + "_" + "Long" + "_" + self.time_msg)

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        # 매도
        elif (Dis_1-DLine)*(Dis-DLine)<0 \
            and c<c1 \
            and Dis_1>Dis \
            and ma5>ma600 \
            and atr1>atr200*1 \
            and v>=va200*2 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "DLINE_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : DLINE" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : DLINE" + "_" + "Short" + "_" + self.time_msg)

            r2 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "DLINE_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "DLINE_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매수 청산
        elif (c-self.doubleSpinBox_2.value())*(c1-self.doubleSpinBox_2.value())<0 \
            and c<c1 \
            and self.Position[0]=="DLINE_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (ma5-ma600)*(ma5-ma600)<0 \
            and c<c1 \
            and self.Position[0]=="DLINE_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif c<=lowest200 \
            and self.Position[0]=="DLINE_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r5 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="DLINE_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r5 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # 매도 청산
        elif (c-self.doubleSpinBox_2.value())*(c1-self.doubleSpinBox_2.value())<0 \
            and c>c1 \
            and self.Position[0]=="DLINE_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r6 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif (ma5-ma600)*(ma5-ma600)<0 \
            and c>c1 \
            and self.Position[0]=="DLINE_Short" \
            and self.Market[0]== market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r7 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif c>=highest200 \
            and self.Position[0]=="DLINE_Short" \
            and self.Market[0]== market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : DLINE"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r8 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="DLINE_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req3", "1103", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : DLINE" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r8 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'DLINE Processing'+'_'+ self.time_msg)

    # Trend : Successive Strong
    def SS(self,market):
        market_ = str(market)
        strategy_ = "SS"
        position_1 = "SELL"
        position_2 = "BUY"
        position_0 = "Clear"
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
            self.Tick = 100
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
            self.Tick = 125000
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
            self.Tick = 1000
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
            self.Tick = 12.5
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거금
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk=str(round(self.kiwoom.account[2],2))

        if self.Margin>0:
            self.po=1
        else:
            self.po=0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))  # 포지션 여부
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0] / 100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1] / 100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        # 가격 데이터 불러오기
        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.MA(df1, 5, 200, 400, 600)
        self.kiwoom.Bolinger(df1, 200, 3)
        self.kiwoom.VA(df1, 600)
        self.kiwoom.ATR(df1, 600)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 600, 100, 5)
        self.kiwoom.V_est(df1,200)

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c_1 = df1['Close'][1]
        c_2 = df1['Close'][2]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        o_1 = df1['Open'][1]
        o_2 = df1['Open'][2]
        v = df1['Volume'][0]
        v_1 = df1['Volume'][1]
        v_2 = df1['Volume'][2]

        ma5 = df1['MA5'][0]
        ma5_1 = df1['MA5'][1]
        ma200 = df1['MA200'][0]
        ma400 = df1['MA400'][0]
        ma600 = df1['MA600'][0]
        bbandsup = df1['BandsUp200_3'][0]
        bbandsdown = df1['BandsDown200_3'][0]
        va600 = df1['VA600'][0]
        atr600 = df1['ATR600'][0]
        atr1 = df1['ATR1'][0]
        atr1_1 = df1['ATR1'][1]
        atr1_2 = df1['ATR1'][2]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU5'][0]
        TD = df1['TD5'][0]
        Highest_volume=df1['V_est200'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량
        Lots1 = self.FullLots1 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots1 = int(Lots1)  # 주문수량
        if int(Lots1)<1:
            self.Lots1=int(1)
        else:
            self.Lots1=int(Lots1)

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량
        Lots2 = self.FullLots2 * self.bet_rate  # 최대주문가능수량 * bet_rate
        self.Lots2 = int(Lots2)  # 주문수량
        if int(Lots2)<1:
            self.Lots2=int(1)
        else:
            self.Lots2=int(Lots2)

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # Risk
        self.Risk_Long1 = round((ma200 - c) * self.Tick, 2)
        self.Risk_Long2 = round((lowest200 - c) * self.Tick, 2)
        self.Risk_Short1 = round((c - ma200) * self.Tick, 2)
        self.Risk_Short2 = round((c - highest200) * self.Tick, 2)

        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(str(self.Risk_Long1)))
        self.tableWidget_2.setItem(1, 0, QTableWidgetItem(str(self.Risk_Long2)))
        self.tableWidget_2.setItem(2, 0, QTableWidgetItem(str(self.Risk_Short1)))
        self.tableWidget_2.setItem(3, 0, QTableWidgetItem(str(self.Risk_Short2)))

        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(self.Risk_Long1 * self.Lots2)))
        self.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(self.Risk_Long2 * self.Lots2)))
        self.tableWidget_2.setItem(2, 1, QTableWidgetItem(str(self.Risk_Short1 * self.Lots2)))
        self.tableWidget_2.setItem(3, 1, QTableWidgetItem(str(self.Risk_Short2 * self.Lots2)))

        # 조건식
        # 매수
        if c>o \
            and c_1>o_1 \
            and c_2>o_2 \
            and v>=va600 \
            and atr1>=atr600*2 \
            and v_1>=va600 \
            and atr1_1>=atr600*2 \
            and v_2>=va600 \
            and atr1_2>=atr600*2 \
            and ma5>ma400 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="SS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : SS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Long" + "_" + self.time_msg)

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_2})

        # 매도
        elif c<o \
            and c_1<o_1 \
            and c_2<o_2 \
            and v >= va600 \
            and atr1 >= atr600 * 2 \
            and v_1 >= va600 \
            and atr1_1 >= atr600 * 2 \
            and v_2 >= va600 \
            and atr1_2 >= atr600 * 2 \
            and ma5<ma400 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "SS_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)

            r2 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_1})

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "SS_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "SS_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "5057928272")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)

        # 매수 청산
        elif ma5<ma400 \
            and self.Position[0]=="SS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : SS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="SS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(market + '_' + "Strategy : SS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Long Position Clear" + "_" + self.time_msg)

            r3 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        # 매도 청산
        elif ma5>ma400 \
            and self.Position[0]=="SS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : SS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.comboBox_5.currentText()=="ON" \
            and int(self.kiwoom.account[1])<0 \
            and int(self.kiwoom.account[2])>int(self.doubleSpinBox_3.value()) \
            and self.Position[0]=="SS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req4", "1104", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")
            self.Market[0] = 'Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem(market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)

            r4 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        else:
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'SS Processing'+'_'+ self.time_msg)

    def Target_limit(self, market):
        market_ = str(market)
        strategy_ = "SS"
        position_1 = "SELL"
        position_2 = "BUY"
        position_0 = "Clear"
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6EU17"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "Pound":
            self.DataCode = "6B000"
            self.OrderCode = self.Code["Pound"]
        elif market == "China":
            self.DataCode = "CN000"
            self.OrderCode = self.Code["China"]
        elif market == "Yen":
            self.DataCode = "6J000"
            self.OrderCode = self.Code["Yen"]
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time

        # 증거금
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.CommRqData("opw30009_req", "opw30009", "", "0101")
        self.Margin = self.kiwoom.state[0]
        self.Risk = str(round(self.kiwoom.account[2], 2))

        if self.Margin > 0:
            self.po = 1
        else:
            self.po = 0

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.po)))  # 포지션 여부
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.account[0]/100)))  # 자산
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.account[1]/100)))  # 손익
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(round(self.kiwoom.account[2], 2))))  # 리스크

        self.kiwoom.SetInputValue("종목코드", self.DataCode)
        self.kiwoom.SetInputValue("시간단위", "10")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c1 = df1['Close'][1]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "1")   # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots1 = self.kiwoom.pos_order[0]  # 주문가능 수량
        self.ClearLots1 = self.kiwoom.pos_order[1]  # 청산가능 수량

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "5057928272")
        self.kiwoom.SetInputValue("비밀번호", "")
        self.kiwoom.SetInputValue("비밀번호입력매체", "")
        self.kiwoom.SetInputValue("종목코드", self.OrderCode)
        self.kiwoom.SetInputValue("매도수구분", "2")  # 1: 매도 2: 매수
        self.kiwoom.SetInputValue("해외주문유형", "2")
        self.kiwoom.SetInputValue("주문표시가격", c)
        self.kiwoom.CommRqData("opw30011_req", "opw30011", "", "1111")
        self.FullLots2 = self.kiwoom.pos_order[2]  # 주문가능 수량
        self.ClearLots2 = self.kiwoom.pos_order[3]  # 청산가능 수량


        # 조건식
        if self.Margin > 0  \
            and self.comboBox_2.currentText() == 'Long' \
            and c < self.doubleSpinBox_2.value():
            self.kiwoom.SendOrder("SendOrder_req", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0", "0",
                                  "1", "0")  # 1:신규매도, 2:신규매수

            r1 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.Margin > 0 \
            and self.comboBox_2.currentText() == 'Short' \
            and c > self.doubleSpinBox_2.value():
            self.kiwoom.SendOrder("SendOrder_req1", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")  # 1:신규매도, 2:신규매수

            r2 = requests.post(self.target_url, data={"value1": market_, "value2": strategy_, "value3": position_0})

        elif self.Margin == 0:
            app = QApplication(sys.argv)
            sys.exit(app)

        else:
            self.listWidget.addItem(market + '_' + str(self.Margin) + '_' + 'Target_Limit Processing' + '_' + self.time_msg)

    def Close(self):
        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time
        app = QApplication(sys.argv)
        sys.exit(app)

    def Corr(self,*args):
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
            self.kiwoom.MA(Data1, 5, 200,400, 600)
            self.kiwoom.Bolinger(Data1, 200, 2.5)
            self.kiwoom.MAX(Data1, 200)
            self.kiwoom.MIN(Data1, 200)

            self.Datalist.append(Data1)
            self.DatalistName.append(x)

        self.Datalen=len(self.DatalistName)
        self.DataSet={}
        for i in range(self.Datalen):
            self.DataSet[self.DatalistName[i]]=self.Datalist[i]['Close']

        DATASET = pd.DataFrame(self.DataSet)
        CORR = pd.DataFrame(DATASET.corr())

        sns.heatmap(data=DATASET.corr(), annot=True,
                    fmt='.2f', linewidths=.5, cmap='Blues')
        plt.show()

if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
