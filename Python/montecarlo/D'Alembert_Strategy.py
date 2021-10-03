import random
import matplotlib
import matplotlib.pyplot as plt
import time

lower_bust=19.00
higher_profit=69.00

sampleSize=1000
startingFunds=10000
wagerSize=100
wagerCount=100

def rollDice():
    roll=random.randint(1,100)

    if roll==100:
        return False
    elif roll<=50:
        return False
    elif 100>roll>=50:
        return True

def dAlembert(funds,initial_wager,wager_count):
    global da_busts
    global da_profits

    value=funds
    wager=initial_wager
    wX=[]
    vY=[]
    currentWager=1
    previousWager='win'
    previousWagerAmount=initial_wager

    while currentWager<=wager_count:
        if previousWager=='win':
            if wager==initial_wager:
                pass
            else:
                wager-=initial_wager

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
                    da_busts+=1
                    break

        elif previousWager=='loss':
            wager=previousWagerAmount+initial_wager
            if (value-wager)<=0:
                wager=value

            if rollDice():
                value+=wager
                previousWager='win'
                wX.append(currentWager)
                vY.append(value)
            else:
                value-=wager
                previousWager='loss'
                previousWagerAmount=wager
                wX.apped(currentWager)
                vY.append(value)

                if value<=0:
                    da_busts+=1
                    break
        currentWager+=1

    if value>funds:
        da_profits+=1
