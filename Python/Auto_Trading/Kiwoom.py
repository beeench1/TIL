
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QAxWidget import *
import time
import pandas as pd
import numpy
import math as m
from technical import MA

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.setControl("KFOPENAPI.KFOpenAPICtrl.1")
        self.connect(self, SIGNAL("OnEventConnect(int)"),self.OnEventConnect)
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString)"), self.OnReceiveTrData)
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"), self.OnReceiveChejanData)

    def CommConnect(self):
        self.dynamicCall("CommConnect(1)")
        self.login_event_loop=QEventLoop()
        self.login_event_loop.exec_()

    def OnEventConnect(self, errCode):
        if errCode==0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def SetInputValue(self,sID,sValue):
        self.dynamicCall("SetInputValue(QString,QString)",sID,sValue)

    def CommRqData(self,RQName,TRCode,PrevNext,ScreenNo):
        self.dynamicCall("CommRqData(QString,QString,QString,QString)",RQName,TRCode,PrevNext,ScreenNo)
        self.tr_event_loop=QEventLoop()
        self.tr_event_loop.exec_()

    def GetCommFullData(self,TrCode,RQName,nGubun):
        data=self.dynamicCall("GetCommFullData(QString,QString,Int)",TrCode,RQName,nGubun)
        return data.strip()

    def GetGlobalFutureCodeByItemMonth(self,sItem,sMonth):  # 종목 코드에 대한 종목명 반환
        ret=self.dynamicCall("GetGlobalFutureCodeByItemMonth(QString,QString)",sItem,sMonth)
        return ret


# OrderType : 주문유형 (1:신규매도, 2:신규매수, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
# HogaGb : 거래구분 (1:시장가, 2:지정가, 3:STOP, 4:STOP LIMIT)
    def SendOrder(self,sRQName, sScreenNo,sAccNo, nOrderType, sCode, nQty, sPrice, sStop, sHogaGb, sOrgOrderNo):
        self.dynamicCall("SendOrder(QString,QString,QString,Int,QString,Int,QString,QString,QString,QString)",[sRQName, sScreenNo,sAccNo, nOrderType, sCode, nQty, sPrice, sStop, sHogaGb, sOrgOrderNo])
        self.order_event_loop=QEventLoop()
        self.order_event_loop.exec_()

    def GetChejanData(self,nFid):
        cmd = 'GetChejanData(%d)' % nFid
        ret=self.dynamicCall(cmd)
        return ret

    def OnReceiveChejanData(self,sGubun,nItemCnt,sFidList):
        print("--------------------------------------------")

        self.order_event_loop.exit()

    def GetLoginInfo(self, sTag):
        cmd = 'GetLoginInfo("%s")' % sTag
        ret = self.dynamicCall(cmd)
        return ret

    def Init_save(self):
        self.minute={'date':[],"Close":[],"High":[],"Low":[],"Open":[],"Volume":[]}
        self.minute_2 = {'date': [], "Close": [], "High": [], "Low": [], "Open": [], "Volume": []}
        self.minute_3 = {'date': [], "Close": [], "High": [], "Low": [], "Open": [], "Volume": []}
        self.minute_4 = {'date': [], "Close": [], "High": [], "Low": [], "Open": [], "Volume": []}

    def Init_State(self):
        self.state=[0,1]

    def Init_Unordered(self):
        self.unordered=[0,1]

    def Init_PosOrder(self):
        self.pos_order=[0,1]

    def OnReceiveTrData(self,ScrNo,RQName,TrCode,RecordName,PreNext):
        self.minute = {'date': [], "Close": [], "High": [], "Low": [], "Open": [], "Volume": []}

        if RQName=="opc10002_req":
            for i in range(600):
                date=i
                Close=self.GetCommData(TrCode,RQName,i,"현재가")
                High=self.GetCommData(TrCode,RQName,i,"고가")
                Low=self.GetCommData(TrCode,RQName,i,"저가")
                Open=self.GetCommData(TrCode,RQName,i,"시가")
                volume=self.GetCommData(TrCode,RQName,i,"거래량")

                self.minute['date'].append(date)
                self.minute['Close'].append(float(Close))
                self.minute['High'].append(float(High))
                self.minute['Low'].append(float(Low))
                self.minute['Open'].append(float(Open))
                self.minute['Volume'].append(int(volume))

        elif RQName=="opw30009_req":
            self.state=[0,1]
            a=self.GetCommData(TrCode,RQName,0,'포지션증거금')
            self.state[0]=int(a)

        elif RQName=="opw30001_req":
            self.unwordered = [0, 1]
            a = self.GetCommData(TrCode, RQName, 0, '주문번호')
            self.unordered[0] = str(a)

        elif RQName=="opw30011_req":
            self.pos_order = [0, 1]
            a = self.GetCommData(TrCode, RQName, 0, '주문가능수량')
            b = self.GetCommData(TrCode, RQName, 0, '청산가능수량')
            self.pos_order[0] = int(a)
            self.pos_order[1] = int(b)
        else:
            print("None req_Name")


        self.tr_event_loop.exit()

    def MA(self,df,n1,n2,n3):
        df['MA'+str(n1)]=pd.rolling_mean(df['Close'],n1)
        df['MA'+str(n2)]=pd.rolling_mean(df['Close'],n2)
        df['MA'+str(n3)]=pd.rolling_mean(df['Close'],n3)

    def Bolinger(self,df,n,d1):
        MA=pd.Series(pd.rolling_mean(df['Close'],n))
        MSD=pd.Series(pd.rolling_std(df['Close'],n))
        b1=MA+(d1*MSD)
        b2=MA-(d1*MSD)
        df['BandsUp'+str(n)+"_"+str(d1)]=b1
        df['BandsDown'+str(n)+"_"+str(d1)]=b2

    def VA(self,df,n):
        df['VA'+str(n)]=pd.rolling_mean(df['Volume'],n)

    def disparity(self,df,n,d1,period1):
        MA=pd.Series(pd.rolling_mean(df['Close'],n))
        disparity=abs(100*(MA-df['Close'])/MA)
        df['disparity'+str(n)]=disparity
        df['dbands']=pd.rolling_mean(disparity,period1)+(pd.rolling_std(disparity,period1)*d1)

    def EMA(self,df, n1,n2,n3):
        EMA1 = pd.ewma(df['Close'], span=n1, min_periods=n1 - 1)
        EMA2 = pd.ewma(df['Close'], span=n2, min_periods=n2 - 1)
        EMA3 = pd.ewma(df['Close'], span=n3, min_periods=n2 - 1)
        df['EMA'+str(n1)]=EMA1
        df['EMA'+str(n2)]=EMA2
        df['EMA' + str(n3)] = EMA3

    def ATR(self,df, n):
        i = 0
        TR_1 = []
        while i<300:
            x=[abs(df['High'][i]-df['Low'][i]),abs(df['High'][i]-df['Close'][i+1]),abs(df['Low'][i]-df['Close'][i+1])]
            TR=max(x)
            TR_1.append(TR)
            i=i+1

        TR_s = pd.Series(TR_1)
        TR_s1=TR_s.sort_index(0,ascending=False)
        ATR = pd.rolling_mean(TR_s1, n)
        df['ATR'+str(n)]=ATR


    def MAX(self,df,period1):
        highest=max(df['Close'][600-period1:600])
        df['highest'+str(period1)]=highest

    def MIN(self, df, period1):
        lowest = min(df['Close'][600-period1:600])
        df['lowest' + str(period1)] = lowest

    def TrailingStop(self,df,period1,x1,p1):
        highest = max(df['Close'][600 - period1:599])
        lowest = min(df['Close'][600 - period1:599])
        TU=highest-(df['ATR'+str(x1)][0]*p1)
        TD=lowest+(df['ATR'+str(x1)][0]*p1)
        df['TU'+str(p1)]=TU
        df['TD'+str(p1)]=TD

    def Crossup(self,A0,A1,B1):
        A0<B1 and A1>B1
        return True

    def Crossdown(self,A0,A1,B1):
        A0 > B1 and A1 < B1




if __name__=="__main__":
    app=QApplication(sys.argv)
    kiwoom=Kiwoom()
    kiwoom.CommConnect()
    kiwoom.save()

    # 데이터 받기
    kiwoom.SetInputValue("종목코드","CL000")
    kiwoom.SetInputValue("시간단위","10")
    kiwoom.CommRqData("opc10002_req","opc10002","","0101")

    df=pd.DataFrame(kiwoom.minute,index=kiwoom.minute['date'],columns=['Close','High','Low','Open','Volume'])
    df1=df.sort_index(0,ascending=False)  # 정렬
    kiwoom.EMA(df1,200,600)
    kiwoom.Bolinger(df1,200,2.5)
    kiwoom.VA(df1,200)
    kiwoom.ATR(df1,100)
    kiwoom.MAX(df1,200)
    kiwoom.MIN(df1,200)
    kiwoom.TrailingStop(df1, 600, 100, 5)


    data=df1

    c=df1['Close'][0]
    h=df1['High'][0]
    l=df1['Low'][0]
    o=df1['Open'][0]
    v=df1['Volume'][0]
    ema200=df1['EMA200'][0]
    ema600=df1['EMA600'][0]
    bbandsup=df1['BandsUp200_2.5'][0]
    bbandsdown=df1['BandsDown200_2.5'][0]
    va200=df1['VA200'][0]
    atr100=df1['ATR100'][0]
    highest200=df1['highest200'][0]
    lowest200=df1['lowest200'][0]
    TU=df1['TU5'][0]
    TD=df1['TD5'][0]

    # 조건식
    if c>=bbandsup and v>va200 and c>ema600:
        kiwoom.SendOrder("SendOrder_req","1101","7022264172",1,"6EH17",1,"0","0","1","0")


    kiwoom.SendOrder("SendOrder_req", "1101", "7002264172", 1, "6EH17", 1, "0", "0", "1", "0")
    print(data)




