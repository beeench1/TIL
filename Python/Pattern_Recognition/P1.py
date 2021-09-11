import numpy as np
from numpy import loadtxt
import time
from functools import reduce
import random



def ch(start,current):
    try:
        ch_=(float(current)-float(start))/float(start)*100
        if ch_==0:
            return 0.00000001
        else:
            return ch_
    
    except:
        return 0.00000001

def Storage(distance,data):
           # distance 기간 움직임
    y=30             # y : 전진값
    dis=distance      # 패턴 간격
    price=data
    currentStance='none'
    x=len(price)-30   # 가격 데이터 길이 - 패턴간격
    
    while y<x:      # 전진값이 커져서 더이상 패턴간격만큼의 패턴을 못만들경우까지
        pattern=[]
        for i in range(1,dis):         
            p=ch(price[y-dis],price[y-dis+i])
            pattern.append(p)
        
        patternAr.append(pattern)
        
        
        currentPoint=price[y]
        outcomeRange=price[distance+20:distance+30]   # 현재 기준 20~30 간격 뒤의 결과값 예측

        try:
            avgOutcome=reduce(lambda x,y : x+y,outcomeRange) /len(outcomeRange)
        except Exception:
            print(str(e))
            avgOutcome=0
        
        futureOutcome=ch(currentPoint,avgOutcome)
        performanceAr.append(futureOutcome)
        
        y+=1

        
def currentPattern(distance,price):
    c_pattern=[]
    for i in range(1,distance):
        c_p=ch(price[-distance],price[i-distance])
        c_pattern.append(c_p)
        c_patternAr.append(c_pattern)

def patternRecognition(distance):
    plotPatAr=[]
    patFound=0
    for i in range(len(data)-distance):
        similar=[]
        for j in range(distance):
            sim= 100 - abs(ch(patternAr[i][j],c_patternAr[j]))
            similar.append(sim)

        howSim=sum(similar)/len(similar)

        if howSim>75:
            patdex=patternAr[i]
            patFound=1
            plotPatAr.append(patdex)

    if patFound==1:

        for i in plotPatAr:
            futurePoints=patternAr.index(i)

        print(performanceAr[futurePoints])
        

patternAr=[]     # 각 pattern을 저장
c_patternAr=[]   # 현재 패턴
performanceAr=[] # 각 pattern의 결과값 저장
data=[]

for i in range(100):
    data.append(random.randint(1,9))

Storage(20,data)
currentPattern(20,data)
#patternRecognition(20)

print(len(patternAr))
print(len(c_patternAr[0]))