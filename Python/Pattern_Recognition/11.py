from functools import reduce

outcomeRange=[1,2,3,4,5]
avgOutcome=reduce(lambda x,y : x+y,outcomeRange) /len(outcomeRange)