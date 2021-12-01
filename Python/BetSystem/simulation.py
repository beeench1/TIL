import random
import matplotlib
import matplotlib.pyplot as plt
import time
import statistics as st
import math

def rollDice(PR):
    roll=random.randint(1,100)

    if roll<=PR:
        return True
    else:
        return False
#Funds : 원금
#PM : 평균수익 PS : 수익표준편차
#LM : 평균손실 LS : 손실표준편차
#PR : 승률
#betrate : 배팅비율
#count : 시행횟수
def simulation(init_capital,EP,EL,PR,RR):
    current=0
    asset=init_capital
    current=0
    count=50
    
    while current<=count:
        Profit=random.gauss(EP,EP/3)
        Loss=random.gauss(EL,EL/3)
        Lot=int(asset*RR/EL)
        if Lot<1: Lot=1
        if rollDice(PR):
            asset=asset+(Profit*Lot)

        else:
            asset=asset-(Loss*Lot)

        current+=1

    result=asset
    
    return result


r_Storage=[]

init_capital=5000
Profit=150
Loss=100
PR=50
sampleSize=500
RR=[0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.2,0.3,0.4,0.5]

for i in RR:
    x=0
    while x<=sampleSize:
        result=simulation(init_capital,Profit,Loss,PR,i)
        r_Storage.append(round(result,2))
        x+=1



    print("RR : ",i)
    print(st.mean(r_Storage))
    print("----------------")