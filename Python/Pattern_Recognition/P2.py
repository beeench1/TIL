from functools import reduce
import random
import openpyxl
import pandas as pd
from openpyxl import load_workbook
import numpy  as np
import pandas as pd

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
        
        
        forward+=1

def CurrentPattern(data,period):
    for i in range(1,period):
        c_p=ch(data[-period],data[i-period])
        c_patternAr.append(round(c_p,2))

def patternRecognition(period):
    patFound=0
    similar = []
    for i in range(len(patternAr)):
        sim= np.corrcoef(patternAr[i],c_patternAr)[0,1]
        similar.append(sim)
        print("AR :"+str(patternAr[i]) + "----"+"CP : "+str(c_patternAr) +"---"+str(sim))

        if sim>0.5:
            sim_pattern=patternAr[i]
            patFound+=1
            plotPatAr.append(sim_pattern)

    print("찾은 패턴 계수 : " + str(patFound))

    
data=[]
patternAr=[]
c_patternAr=[]
plotPatAr=[]

wb=load_workbook("aa.xlsx",data_only=True)
ws=wb['Sheet1']

for row in ws['A1':'A100']:
    for cell in row:
        data.append(cell.value)
        
Storage(data,30,30)
CurrentPattern(data,30)
patternRecognition(30)

print("패턴 리스트의 개수 : "+ str(len(patternAr)))
print("패턴당 데이터 수 :" + str(len(patternAr[0])))
print("현재 패턴의 데이터 수 :" + str(len(c_patternAr)))
print(patternAr[0])
print(c_patternAr)
print(plotPatAr)
print(data)
