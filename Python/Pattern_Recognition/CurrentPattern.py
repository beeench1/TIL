
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

def CurrentPattern(data,period):
    c_pattern=[]
    for i in range(1,period):
        c_p=ch(data[-period],data[i-period])
        c_pattern.append(c_p)
    
    c_patternAr.append(c_pattern)

c_patternAr=[]
data=[]

for i in range(100):
    data.append(random.randint(1,9))

CurrentPattern(data,20)
print(len(c_patternAr[0]))
print(len(c_patternAr))
