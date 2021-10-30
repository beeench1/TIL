import random
import matplotlib
import matplotlib.pyplot as plt
import time
from statistics import mean



def rollDice():
    roll=random.randint(1,100)

    if roll==100:
        return False
    elif roll<=50:
        return False
    elif 100>roll>=50:
        return True

def multiple_bettor(funds,initial_wager,wager_count):

    global multiple_busts
    global multiple_profits

    value=funds
    wager=initial_wager
    wX=[]
    vY=[]
    currentWager=1
    previousWager='win'
    previousWagerAmount=initial_wager

    while currentWager<=wager_count:
        if previousWager=='win':
            if rollDice():
                value+=wager
                wX.append(currentWager)
                vY.append(value)

            else:
                value-=wager
                previousWager='loss'
                previousWagerAmount=wager
                wX.append(currentWager)
                vY.append(value)
                if value<=0:
                    multiple_busts+=1
                    break
        elif previousWager=='loss':
            if rollDice():
                wager=previousWagerAmount*random_multiple
                if (value-wager)<=0:
                    wager=value

                value+=wager
                wager=initial_wager
                previousWager='win'
                wX.append(currentWager)
                vY.append(value)
            else:
                wager=previousWagerAmount*random_multiple
                if (value-wager)<=0:
                    wager=value
                value-=wager
                previousWager='loss'
                previousWagerAmount=wager
                wX.append(currentWager)
                vY.append(value)

                if value<=0:
                    multiple_busts+=1
                    break

        currentWager+=1

    if value>funds:
        multiple_profits+=1

# 설정값
lower_bust=31.235
higher_profit=63.208

sampleSize=1000
startingFunds=10000
wagerSize=100
wagerCount=100

X=[]
x=0
while x<10000:
    multiple_busts=0.0
    multiple_profits=0.0
    multipleSampleSize=1000
    currentSample=1


    random_multiple=random.uniform(0.1,10.0)
    while currentSample<=multipleSampleSize:
        multiple_bettor(startingFunds,wagerSize,wagerCount)
        currentSample+=1

    if ((multiple_busts/multipleSampleSize)*100<lower_bust) and ((multiple_profits/multipleSampleSize)*100>higher_profit):
        X.append(random_multiple)
        print(('#####################################'))
        print(('found a winner, the multiple was: ',random_multiple))
        print(('Lower Bust Rate Than: ',lower_bust))
        print(('Higher profit rate than: ',higher_profit))
        print(('Bust Rate: ',(multiple_busts/multipleSampleSize)*100.00))
        print(('Profit Rate: ',(multiple_profits/multipleSampleSize)*100))
        print(('#####################################'))
        time.sleep(5)
    else:
        pass

    x+=1


print(mean(X))





