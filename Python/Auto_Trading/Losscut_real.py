import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Kiwoom1 import *
from concurrent.futures import ProcessPoolExecutor
import functools
import threading

form_class = uic.loadUiType("pytrader5.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom1()
        self.kiwoom.CommConnect()

        self.Code = {"Gold": "MGCQ17",
                     "Euro": "M6EU17",
                     "Oil": "QMZ17",
                     "AUD": "6AH17"}  # 주문코드

        self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'wt')
        self.pushButton.clicked.connect(self.timeout)

    def timeout(self):

        # 시간
        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time
        self.listWidget_6.addItem("Started on" + "_" + self.time_msg)
        self.fw.write("Start Time :" + self.time_msg)
        self.fw.write('\n')

        # 시스템 시작 전 시장 포지션 설정
        '''
                Market : Gold, Euro, Oil, AUD, CAD
                Position : bbands_Long, bbands_Short, R_est_Long, R_est_Short
        '''

        self.Holding = self.comboBox.currentText()
        self.exe()

    def exe(self):
        self.timer_0 = QTimer(self)
        self.timer_0.start(600000)  # 1000 = 1초

        '''

        1. Target_limit
           - Input : 손실제한가격

        2. Risk_limit
           - Input : 리스크한도

        3. Technical_limit
           - Input : 지표

        '''

        timerCallback1 = functools.partial(self.Target_limit, market=self.Holding)

        exe_1 = self.timer_0.timeout.connect(timerCallback1)

        exe = ProcessPoolExecutor(max_workers=5)
        exe.submit(exe_1)

    # Strategy : bbands
    def Target_limit(self, market):
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6EU17"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "AUD":
            self.DataCode = "6A000"
            self.OrderCode = self.Code["AUD"]
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

            self.fw.write(market + '_' + "Target_limit is cleared" + "_" + self.time_msg)
            self.fw.write('\n')

        elif self.Margin > 0 \
            and self.comboBox_2.currentText() == 'Short' \
            and c > self.doubleSpinBox_2.value():
            self.kiwoom.SendOrder("SendOrder_req1", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0", "0",
                                  "1", "0")  # 1:신규매도, 2:신규매수

            self.fw.write(market + '_' + "Target_limit is cleared" + "_" + self.time_msg)
            self.fw.write('\n')

        elif self.Margin == 0:
            app = QApplication(sys.argv)
            sys.exit(app)

        else:
            self.listWidget.addItem('Target_limit is Processing' + '_' + self.time_msg)

    def Risk_limit(self, market):
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "AUD":
            self.DataCode = "6A000"
            self.OrderCode = self.Code["AUD"]
        else:
            self.listWidget.addItem("Code Initialize Failed")

        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time6

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
        self.kiwoom.SetInputValue("매도수구분", "1")  # 1: 매도 2: 매수
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
        if self.Margin > 0 \
            and self.kiwoom.account[1]<0 \
            and round(self.kiwoom.account[2], 2) > self.doubleSpinBox_2.value():
            if self.comboBox_2.currentText() == 'Long':
                self.kiwoom.SendOrder("SendOrder_req", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0",
                                      "0","1", "0")  # 1:신규매도, 2:신규매수

            elif self.comboBox_2.currentText() ==  'Short':
                self.kiwoom.SendOrder("SendOrder_req1", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0", "1", "0")  # 1:신규매도, 2:신규매수

            self.fw.write(market + '_' + "Risk_limit is cleared" + "_" + self.time_msg)
            self.fw.write('\n')

        elif self.Margin==0:
            app = QApplication(sys.argv)
            sys.exit(app)

        else:
            self.listWidget.addItem('Risk_limit is Processing' + '_' + self.time_msg)

    def Technical_limit(self, market):
        if market == "Gold":
            self.DataCode = "GC000"
            self.OrderCode = self.Code["Gold"]
        elif market == "Euro":
            self.DataCode = "6E000"
            self.OrderCode = self.Code["Euro"]
        elif market == "Oil":
            self.DataCode = "CL000"
            self.OrderCode = self.Code["Oil"]
        elif market == "AUD":
            self.DataCode = "6A000"
            self.OrderCode = self.Code["AUD"]
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
        self.kiwoom.EMA(df1, 5, 200, 600)
        self.kiwoom.Bolinger(df1, 200, 2.5)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 100)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 600, 100, 5)
        self.kiwoom.V_est(df1, 200)

        # 가격 데이터 인덱싱
        c = df1['Close'][0]
        c1 = df1['Close'][1]
        h = df1['High'][0]
        l = df1['Low'][0]
        o = df1['Open'][0]
        v = df1['Volume'][0]

        ema5 = df1['EMA5'][0]
        ema5_1 = df1['EMA5'][1]
        ema200 = df1['EMA200'][0]
        ema600 = df1['EMA600'][0]
        bbandsup = df1['BandsUp200_2.5'][0]
        bbandsdown = df1['BandsDown200_2.5'][0]
        va200 = df1['VA200'][0]
        atr100 = df1['ATR100'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU5'][0]
        TD = df1['TD5'][0]
        Highest_volume = df1['V_est200'][0]

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
        if self.Margin > 0 \
             and (ema5-ema200)*(ema5_1-ema200)<0 \
             and ema5<ema5_1 \
             and self.comboBox_2.currentText() == 'Long':
                self.kiwoom.SendOrder("SendOrder_req", "1101", "5057928272", 1, self.OrderCode, self.ClearLots1, "0",
                                      "0", "1", "0")  # 1:신규매도, 2:신규매수
                self.fw.write(market + '_' + "Technical_limit is cleared" + "_" + self.time_msg)
                self.fw.write('\n')

        elif self.Margin > 0 \
            and (ema5-ema200)*(ema5_1-ema200)<0 \
            and ema5>ema5_1 \
            and self.comboBox_2.currentText() == 'Short':
                self.kiwoom.SendOrder("SendOrder_req1", "1102", "5057928272", 2, self.OrderCode, self.ClearLots2, "0",
                                      "0", "1", "0")  # 1:신규매도, 2:신규매수
                self.fw.write(market + '_' + "Technical_limit is cleared" + "_" + self.time_msg)
                self.fw.write('\n')

        elif self.Margin == 0:
            app = QApplication(sys.argv)
            sys.exit(app)

        else:
            self.listWidget.addItem('Technical_limit is Processing' + '_' + self.time_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
