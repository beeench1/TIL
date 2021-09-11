from functools import reduce
import random
import openpyxl
import pandas as pd
from openpyxl import load_workbook
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

def ch(start,current):
    try:
        ch_=(float(current)-float(start))/float(start)*100
        if ch_==0:
            return 0.00000001
        else:
            return ch_
    
    except:
        return 0.00000001


def Storage(data,period,forward):
    currentStance='none'
    x=len(data)-period   # 가격 데이터 길이 - 패턴간격
    
    while forward<x:      # 전진값이 커져서 더이상 패턴간격만큼의 패턴을 못만들경우까지
        pattern=[]
        for i in range(1,period):         
            p=ch(data[forward-period],data[forward-period+i])
            pattern.append(round(p,2))
        
        patternAr.append(pattern)

        currentPoint=data[forward]
        outcomeRange=data[forward+20:forward+30]   # 현재 기준 20~30 간격 뒤의 결과값 예측

        try:
            avgOutcome=reduce(lambda x,y : x+y,outcomeRange) /len(outcomeRange)
        except Exception:
            print(str(e))
            avgOutcome=0
        
        futureOutcome=ch(currentPoint,avgOutcome)
        performanceAr.append(round(futureOutcome,2))
        
        forward+=1

def CurrentPattern(data,period):
    for i in range(1,period):
        c_p=ch(data[-period],data[i-period])
        c_patternAr.append(round(c_p,2))

def patternRecognition(period):
    patFound=0
    for i in range(len(patternAr)):
        sim= np.corrcoef(patternAr[i],c_patternAr)[0,1]
        similar.append(round(sim,2))
        print("AR :"+str(patternAr[i]) + "----"+"CP : "+str(c_patternAr) +"---"+str(sim))

        if sim>0.5:
            sim_pattern=patternAr[i]
            plotPatAr.append(sim_pattern)
            plotPatCor.append(round(sim,2))
            plotPatIndex.append(i)
        patFound+=1

    print("찾은 패턴 계수 : " + str(patFound))
    return patFound

similar=[]
data=[]             # 데이터 
patternAr=[]        # 패턴 추출 저장
performanceAr=[]    # 패턴의 미래 수익
c_patternAr=[]      # 현시점 패턴
plotPatAr=[]        # 유사한 패턴 저장
plotPatCor=[]          # 유사패턴 상관계수
plotPatIndex=[]     # 유사패턴 인덱스

wb=load_workbook("aa.xlsx",data_only=True)
ws=wb['Sheet1']

for row in ws['A1':'A100']:
    for cell in row:
        data.append(cell.value)
        
Storage(data,30,30)
CurrentPattern(data,30)
patternRecognition(30)


print("패턴 리스트의 개수 : "+ str(len(patternAr)))
print("패턴의 수익률 :" + str(len(performanceAr)))
print("패턴당 데이터 수 :" + str(len(patternAr[0])))
print("현재 패턴의 데이터 수 :" + str(len(c_patternAr)))
#print(performanceAr)
#print(c_patternAr)
#print(plotPatAr)
#print(data)

'''
for i in range(len(plotPatAr)):
    plt.figure(i)
    plt.plot(c_patternAr,color='red',label='Current')
    plt.plot(plotPatAr[i],color='green',label='Past')
    plt.xlabel('period')
    plt.ylabel('ch')
    plt.text(20,1,str(plotPatCor[i]))
    plt.legend(loc="lower right",ncol=1)
    plt.show()
'''

for i in plotPatIndex:
    FoundedPat=patternAr[i]
    plt.figure(i)
    plt.plot(c_patternAr,color='red',label='Current')
    plt.plot(FoundedPat,color='green',label='Past')
    plt.xlabel('period')
    plt.ylabel('ch')
    plt.text(25,(plt.ylim()[1]-plt.ylim()[0])/3,"COR :" + str(similar[i]))
    plt.text(25,(plt.ylim()[1]-plt.ylim()[0])*2/3,"Profit(%) : " + str(performanceAr[i]))
    plt.scatter(35,performanceAr[i],c='#24bc00',alpha=0.4)
    plt.legend(loc="lower right",ncol=1)
    plt.show()
    

