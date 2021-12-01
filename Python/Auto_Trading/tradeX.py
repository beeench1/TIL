import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Kiwoom1 import *
from concurrent.futures import ProcessPoolExecutor
import functools
import threading


form_class=uic.loadUiType("pytrader4.ui")[0]

class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom=Kiwoom1()
        self.kiwoom.CommConnect()

        self.Code = {"Gold": "GCZ17",
                     "Euro": "6EU17",
                     "Oil": "CLV17",
                     "AUD": "6AH17"}  # 주문코드

        self.fw=open('C:\\Users\dabee\Desktop\history.txt', 'a+')
        self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
        self.pushButton.clicked.connect(self.timeout)
        self.pushButton_2.clicked.connect(self.Close)

    def timeout(self):

        # 시간
        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time
        self.listWidget_6.addItem("Started on" + "_" + self.time_msg)
        self.fw.write("------------------------------------------------")
        self.fw.write('\n')
        self.fw.write("Start Time :" + self.time_msg)
        self.fw.write('\n')
        self.fw.close()
        self.fw2.write("------------------------------------------------")
        self.fw2.write('\n')
        self.fw2.write("Start Time :" + self.time_msg)
        self.fw2.write('\n')
        self.fw2.close()

        # 시스템 시작 전 초기 설정값
        '''
                Market : Gold, Euro, Oil, AUD, CAD
                Position : bbands_Long, bbands_Short, R_est_Long, R_est_Short, BB_TS_Long, BB_TS_Short
        '''

        self.Market = [self.comboBox.currentText(), 1]
        self.Position = [self.comboBox_2.currentText(), 1]
        self.bet_rate=self.doubleSpinBox.value()

        self.Holding = self.comboBox.currentText()
        self.exe()

    def exe(self):
        self.timer_0 = QTimer(self)
        self.timer_0.start(60000)  # 1000 = 1초

        '''
        BBANDS
        BB_TS
        R_est
        SS
        '''

        timerCallback2 = functools.partial(self.SS, market="Oil")

        exe_2 = self.timer_0.timeout.connect(timerCallback2)


        exe = ProcessPoolExecutor(max_workers=5)
        exe.submit(exe_2)



    # Trend : bbands
    def BBANDS(self,market):
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
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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
        self.kiwoom.EMA(df1, 5, 200, 600)
        self.kiwoom.Bolinger(df1, 200, 3)
        self.kiwoom.VA(df1, 200)
        self.kiwoom.ATR(df1, 200)
        self.kiwoom.ATR(df1, 1)
        self.kiwoom.MAX(df1, 200)
        self.kiwoom.MIN(df1, 200)
        self.kiwoom.TrailingStop(df1, 600, 100, 5)
        self.kiwoom.V_est(df1,200)

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

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # bbands 전략 조건식
        # 매수
        if (c-bbandsup)*(c1-bbandsup)<0 \
            and c>bbandsup \
            and c>o \
            and c>ema200 \
            and v>=va200*2 \
            and c>=highest200 \
            and atr1>=atr200*4 \
            and self.comboBox_3.currentText()=="ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="bbands_Long"
            self.listWidget.addItem(market+"_"+"Strategy : Bolinger Bands"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : Bolinger Bands"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도
        elif (c-bbandsdown)*(c1-bbandsdown)<0 \
            and c<bbandsdown \
            and c<o \
            and c<ema200 \
            and v>=va200*2 \
            and c<=lowest200 \
            and atr1>=atr200*4 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "bbands_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market +"_"+ "Strategy : Bolinger Bands" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "bbands_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "bbands_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매수 청산
        elif ema5<ema200 \
            and self.Position[0]=="bbands_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : Bolinger Bands"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : Bolinger Bands"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()


        # 매도 청산
        elif ema5>ema200 \
            and self.Position[0]=="bbands_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : Bolinger Bands"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : Bolinger Bands" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : Bolinger Bands"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_'+ str(self.Margin) +'_'+'BBANDS Processing'+'_'+ self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'BBANDS Processing'+'_'+ self.time_msg)
            self.fw2.close()

    # Reversal : Bolinger Bands Trailing Stop
    def BB_TS(self,market):
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
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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
        self.kiwoom.SetInputValue("시간단위", "1")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.EMA(df1, 5, 200, 600)
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

        ema5 = df1['EMA5'][0]
        ema5_1 = df1['EMA5'][1]
        ema200 = df1['EMA200'][0]
        ema600 = df1['EMA600'][0]
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
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # BB_TS 전략 조건식
        # 매수
        if (c-BTD200)*(o-BTD200)<0 \
            and c>BTD200 \
            and c>o \
            and ema5<ema600 \
            and v>=va200 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="BBTS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : BBTS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : BBTS"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도
        elif (c-BTU200)*(o-BTU200)<0 \
            and c<BTU200 \
            and c<o \
            and ema5>ema600 \
            and v>=va200 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "BBTS_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market +"_"+ "Strategy : BBTS" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "BBTS_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "BBTS_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매수 청산
        elif (ema5-ema600)*(ema5_1-ema600)<0 \
            and ema5<ema5_1 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        elif c<=lowest200 \
            and self.Position[0]=="BBTS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BBTS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()


        # 매도 청산
        elif (ema5-ema600)*(ema5_1-ema600)<0 \
            and ema5>ema5_1 \
            and self.Position[0]=="BBTS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BBTS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        elif c>=highest200 \
            and self.Position[0]=="BBTS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : BBTS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : BBTS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BBTS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_' + str(self.Margin) + '_' + 'BBTS Processing' + '_' + self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'BBTS Processing'+'_'+ self.time_msg)
            self.fw2.close()

    # Reversal : R.-est
    def R_est(self,market):
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
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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
        self.kiwoom.EMA(df1, 5, 200, 600)
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
        bbandsup = df1['BandsUp200_3'][0]
        bbandsdown = df1['BandsDown200_3'][0]
        va200 = df1['VA200'][0]
        atr200 = df1['ATR200'][0]
        atr1 = df1['ATR1'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        lowest600 = df1['lowest600'][0]
        highest600 = df1['highest600'][0]

        TU6 = df1['TU6'][0]
        TD6 = df1['TD6'][0]
        Highest_volume=df1['V_est200'][0]
        BTU200= df1['BTU']
        BTD200 = df1['BTD']

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # R_est 전략 조건식
        # 매수
        if (ema5-TD6)*(ema5_1-TD6)<0 \
            and ema5>TD6 \
            and ema5>ema5_1 \
            and atr1>atr200*4 \
            and v>=va200*2 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="R_est_Long"
            self.listWidget.addItem(market+"_"+"Strategy : R_est"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : R_est" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : R_est"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도
        elif (ema5-TU6)*(ema5_1-TU6)<0 \
            and ema5<TU6 \
            and ema5<ema5_1 \
            and atr1>atr200*4 \
            and v>=va200*2 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "R_est_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : R_est" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : R_est" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market +"_"+ "Strategy : R_est" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "R_est_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "R_est_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매수 청산
        elif (ema5-ema600)*(ema5_1-ema600)<0 \
            and ema5<ema5_1 \
            and self.Position[0]=="R_est_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : R_est"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : R_est" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : R_est"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        elif c<=lowest600 \
            and self.Position[0]=="R_est_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1102", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : R_est"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : R_est" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : R_est"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()


        # 매도 청산
        elif (ema5-ema600)*(ema5_1-ema600)<0 \
            and ema5>ema5_1 \
            and self.Position[0]=="R_est_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : R_est"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : R_est" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : R_est"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        elif c>=highest600 \
            and self.Position[0]=="R_est_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1102", "7002264172", 1, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : R_est"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : R_est" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : R_est"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_' + str(self.Margin) + '_' + 'R_est Processing' + '_' + self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'R_est Processing'+'_'+ self.time_msg)
            self.fw2.close()

    # Trend : Successive Strong
    def SS(self,market):
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
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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
        self.kiwoom.SetInputValue("시간단위", "1")
        self.kiwoom.CommRqData("opc10002_req", "opc10002", "", "0101")

        df = pd.DataFrame(self.kiwoom.minute, index=self.kiwoom.minute['date'],
                          columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        df1 = df.sort_index(0, ascending=False)  # 정렬
        self.kiwoom.EMA(df1, 5, 200, 600)
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

        ema5 = df1['EMA5'][0]
        ema5_1 = df1['EMA5'][1]
        ema200 = df1['EMA200'][0]
        ema600 = df1['EMA600'][0]
        bbandsup = df1['BandsUp200_3'][0]
        bbandsdown = df1['BandsDown200_3'][0]
        va600 = df1['VA600'][0]
        atr600 = df1['ATR600'][0]
        atr1 = df1['ATR1'][0]
        highest200 = df1['highest200'][0]
        lowest200 = df1['lowest200'][0]
        TU = df1['TU5'][0]
        TD = df1['TD5'][0]
        Highest_volume=df1['V_est200'][0]

        # 주문가능수량 조회(매도)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        # 주문가능수량 조회(매수)
        self.kiwoom.SetInputValue("계좌번호", "7002264172")
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

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.Lots2)))

        # 조건식
        # 매수
        if c>o \
            and c_1>o_1 \
            and c_2>o_2 \
            and v>=va600*2 \
            and v_1>=va600*2 \
            and v_2>=va600*2 \
            and c>ema200 \
            and self.comboBox_3.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 2, self.OrderCode, self.Lots2, "0", "0", "1", "0")
            self.Market[0]=market
            self.Position[0]="SS_Long"
            self.listWidget.addItem(market+"_"+"Strategy : SS"+"_"+"Long"+"_"+self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Long" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+"_"+"Strategy : SS"+"_"+"Long"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도
        elif c<o \
            and c_1<o_1 \
            and c_2<o_2 \
            and v>=va600*2 \
            and v_1>=va600*2 \
            and v_2>=va600*2 \
            and c<ema200 \
            and self.comboBox_4.currentText() == "ON" \
            and self.Position[0] == 'Nothing' \
            and self.Margin==0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.Lots1, "0", "0", "1","0")
            self.Market[0] = market
            self.Position[0] = "SS_Short"
            self.listWidget.addItem(market +"_"+ "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.listWidget_2.addItem(market + "_" + "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market +"_"+ "Strategy : SS" + "_" + "Short" + "_" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 주문이 이뤄지지 않았을 때

        # 매수 취소
        elif self.Margin == 0 and self.Position[0] == "SS_Long" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "2")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 4, self.OrderCode, self.Lots2, str(c), "0", "2",self.OrderNo)
            self.Market[0]='Nothing'
            self.Position[0] = 'Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매도 취소
        elif self.Margin == 0 and self.Position[0] == "SS_Short" and self.Market[0]==market:
            self.kiwoom.SetInputValue("계좌번호", "7002264172")
            self.kiwoom.SetInputValue("비밀번호", "")
            self.kiwoom.SetInputValue("비밀번호입력매체", "")
            self.kiwoom.SetInputValue("종목코드", self.OrderCode)
            self.kiwoom.SetInputValue("통화코드", "USD")
            self.kiwoom.SetInputValue("매도수구분", "1")
            self.kiwoom.CommRqData("opw30001_req", "opw30001", "", "1111")
            self.OrderNo = self.kiwoom.unordered[0]

            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 3, self.OrderCode, self.Lots1, str(c), "0", "2",self.OrderNo)
            self.Market[0] = 'Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem("Canceled" + self.time_msg)
            self.listWidget_2.addItem("Canceled" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write("Canceled" + self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        # 매수 청산
        elif ema5<ema200 \
            and self.Position[0]=="SS_Long" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, self.OrderCode, self.ClearLots1, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : SS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Long Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : BSS"+"_"+"Long Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()


        # 매도 청산
        elif ema5>ema200 \
            and self.Position[0]=="SS_Short" \
            and self.Market[0]==market \
            and self.Margin>0:
            self.kiwoom.SendOrder("SendOrder_req", "1102", "7002264172", 2, self.OrderCode, self.ClearLots2, "0", "0", "1", "0")
            self.Market[0]='Nothing'
            self.Position[0]='Nothing'
            self.listWidget.addItem(market+'_'+"Strategy : SS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.listWidget_2.addItem(
                market + '_' + "Strategy : SS" + "_" + "Short Position Clear" + "_" + self.time_msg)
            self.fw = open('C:\\Users\dabee\Desktop\history.txt', 'a+')
            self.fw.write(market+'_'+"Strategy : SS"+"_"+"Short Position Clear"+"_"+self.time_msg)
            self.fw.write('\n')
            self.fw.close()

        else:
            self.fw2 = open('C:\\Users\dabee\Desktop\history2.txt', 'a+')
            self.fw2.write(market + '_' + str(self.Margin) + '_' + 'SS Processing' + '_' + self.time_msg)
            self.fw2.write('\n')
            self.listWidget.addItem(market + '_'+ str(self.Margin) +'_'+'SS Processing'+'_'+ self.time_msg)
            self.fw2.close()

    def Close(self):
        self.current_time = QTime.currentTime()
        self.text_time = self.current_time.toString("hh:mm:ss")
        self.time_msg = self.text_time
        self.fw.write("End Time :" + self.time_msg)
        app = QApplication(sys.argv)
        sys.exit(app)


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
