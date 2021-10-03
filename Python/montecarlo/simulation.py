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
def simulation(init_capital,EP,EL,PR):
    current=0
    asset=init_capital
    current=0
    count=50
    
    while current<=count:
        Profit=random.gauss(EP,EP/3)
        Loss=random.gauss(EL,EL/3)
        if rollDice(PR):
            asset=asset+Profit

        else:
            asset=asset-Loss

        current+=1

    result=asset
    
    return result


r_Storage=[]

init_capital=5000
Profit=200
Loss=100
PR=50
sampleSize=500

x=0
while x<=sampleSize:
    result=simulation(init_capital,Profit,Loss,PR)
    r_Storage.append(round(result,2))
    x+=1



print(r_Storage)
print(st.median(r_Storage))