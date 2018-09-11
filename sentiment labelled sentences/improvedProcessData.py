#import math as m 
import re

def readToDict(filename):
    allClasses = {}
    for line in open(filename):
        cleanLine = re.sub(r"[\n\t!';:&*():?%$#+]","",line.lower())
        review = re.sub(r"[/,.-]"," ",cleanLine)
        val = int(review[-1][-1])
        if val in allClasses:
            allClasses[val].append(review[:-1])
    
        else:
            allClasses[val] = [review[:-1]]
    return(allClasses)

def posDict(allClasses):
    posClass = {}
    for line in allClasses[1]:
        for word in line.split(): 
            if word in posClass :
                posClass[word]+=1
    
            else:
                posClass[word] = 1
   return posClass

def negDict(allClasses):
    negClass = {}
    for line in allClasses[0]:
        for word in line.split(): 
            if word in negClass :
                negClass[word]+=1
    
            else:
                negClass[word] = 1
    return negClass
    
def totalDict(posDict, negDict):
    totalDict = posDict.copy()   # start with x's keys and values
    for key in negDict:
        if key in totalDict:
            totalDict[key] += negDict[key]
        else:
            totalDict[key] = negDict[key]
            
       
    return totalDict 

allClasses = readToDict('amazon_cells_labelled.txt')
countP, posClass = posDict(allClasses)
countN, negClass = negDict(allClasses)
totalDict = totalDict(posClass, negClass)
