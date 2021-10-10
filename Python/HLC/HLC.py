import openpyxl
import pandas as pd
from openpyxl import load_workbook
import statistics as st

def HLC(df):
    a1=[]
    for i in range(len(df)):
        HLC=(df['high'][i]+df['low'][i]+df['close'][i])/3
        a1.append(round(HLC,0))
            
    HLC_=pd.Series(a1)
    df['HLC']=HLC_

def ch_(start,current):
    try:
        ch_=100*(float(current)-float(start))/float(start)
        if ch_==0:
            return 0.00000001
        else:
            return ch_
    
    except:
        return 0.00000001

def initPat_L(df,period):
    patternStorage=[]
    patternProfit=[]
    for i in range(3,len(df)-period-1):
        if df['HLC'][i-1]>df['high'][i-2]:
            patternStorage.append(df['open'][i])
            profit=ch_(df['open'][i],df['close'][i+period])
            patternProfit.append(round(profit,2))

    return patternStorage,patternProfit

def initPat_S(df,period):
    patternStorage=[]
    patternProfit=[]
    for i in range(3,len(df)-period-1):
        if df['HLC'][i-1]<df['low'][i-2]:
            patternStorage.append(df['date'][i])
            profit=ch_(df['open'][i],df['close'][i+period])
            patternProfit.append(round(profit,2))

    return patternStorage,patternProfit

# A : 시간 / B: 시가 / C : 고가  / D : 저가   / E : 종가
Close=[]
High=[]
Low=[]
Open=[]
Date=[]

wb=load_workbook("goldDay.xlsx",data_only=True)
col0=wb['Sheet1']['A'][1:]  # Date
col1=wb['Sheet1']['C'][1:]   # High
col2=wb['Sheet1']['D'][1:]  # Low
col3=wb['Sheet1']['E'][1:]  # Close
col4=wb['Sheet1']['B'][1:]   # Open

for cell in col0:
    if cell.value==None:
        break
    else:
        Date.append(cell.value)

for cell in col1:
    if cell.value==None:
        break
    else:
        High.append(cell.value)

for cell in col2:
    if cell.value==None:
        break
    else:
        Low.append(cell.value)

for cell in col3:
    if cell.value==None:
        break
    else:
        Close.append(cell.value)

for cell in col4:
    if cell.value==None:
        break
    else:
        Open.append(cell.value)

raw_data={'date':Date,    'close':Close,  'high':High,    'low':Low     ,'open':Open}
df=pd.DataFrame(raw_data)
HLC(df)


# period=[1,2,3,5,8,13]

# for i in period:
#     x=initPat_L(df,i)
#     m=round(st.mean(x[1]),2)
#     win,lose=[],[]
#     for j in x[1]:
#         if j>0:
#             win.append(j)
#         else:
#             lose.append(j)
    
#     pr=round(len(win)/(len(win)+len(lose)),2)
    
#     print('==========================')
#     print("(L)샘플:" + str(len(x[1])))
#     print("예측기간 :" + str(i))
#     print('승률 :' +    str(pr) )
#     print('수익률 :' + str(m))

# for i in period:
#     x=initPat_S(df,i)
#     m=round(st.mean(x[1]),2)
#     win,lose=[],[]
#     for j in x[1]:
#         if j>0:
#             win.append(j)
#         else:
#             lose.append(j)
    
#     pr=round(len(lose)/(len(win)+len(lose)),2)
    
#     print('==========================')
#     print('(S)샘플:' + str(len(x[1])))
#     print('예측기간 :' + str(i))
#     print('승률 :' +    str(pr) )
#     print('수익률 :' + str(m))

def simulation(df,ref,ref_c):
    cnt=0
    position=False

    profit=[]
    phold=[]
    loss=[]
    lhold=[]
    for i in range(3,len(df)-1):
        
        if df['HLC'][i-1]>df['high'][i-2] and position==False:
            position=True
            entry=df['open'][i]
            cnt+=1
            
        elif position==True and ch_(entry,df['close'][i])>ref:
            profit.append(ch_(entry,df['close'][i]))
            phold.append(cnt)
            cnt=0
            entry=0
            position=False

        elif position==True and ch_(entry,df['close'][i])<ref_c:
            loss.append(ch_(entry,df['close'][i]))
            lhold.append(cnt)
            cnt=0
            entry=0
            position=False

        elif position==True:
            cnt+=1

        elif position==False:
            cnt+=0

    pr=round(len(profit)/(len(profit)+len(loss)),2)    
    profit=round(st.mean(profit),2)
    phold=round(st.mean(phold),2)
    loss=round(st.mean(loss),2)
    lhold=round(st.mean(lhold),2)
    
    print("수익(%) :" + str(profit))
    print("수익 보유기간 :" + str(phold)) 
    print("손실(%) :" + str(loss))   
    print("수익 보유기간 :" + str(lhold))        
    print("승률 :" + str(pr))



simulation(df,1.0,-0.5)