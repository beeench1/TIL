
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


def Storage(data,period,forward):
    currentStance='none'
    x=len(data)-period   # 가격 데이터 길이 - 패턴간격
    
    while forward<x:      # 전진값이 커져서 더이상 패턴간격만큼의 패턴을 못만들경우까지
        pattern=[]
        for i in range(1,period):         
            p=ch(data[forward-period],data[forward-period+i])
            pattern.append(p)
        
        patternAr.append(pattern)
        
        '''
        currentPoint=p[period]
        outcomeRange=p[period+20:period+30]   # 현재 기준 20~30 간격 뒤의 결과값 예측

        try:
            avgOutcome=reduce(lambda x,y : x+y,outcomeRange) /len(outcomeRange)
        except Exception:
            print(str(e))
            avgOutcome=0
        
        futureOutcome=ch(currentPoint,avgOutcome)
        performanceAr.append(futureOutcome)
        '''
        forward+=1

patternAr=[]
performanceAr=[]
data=[]

for i in range(100):
    data.append(random.randint(1,9))

Storage(data,20,20)
print(len(patternAr[0]))
print(len(patternAr))
