import numpy as np
import re
from collections import Counter
from itertools import chain

def readToDict(*filenames):
    allClasses = {}
    for filename in filenames:
        for line in open(filename):
            cleanLine = re.sub(r"[\n\t!';:&*():?%$#+]","",line.lower())
            review = re.sub(r"[/,.-]"," ",cleanLine)
            val = int(review[-1][-1])
            if val in allClasses:
                allClasses[val].append(review[:-1].split())
            else:
                allClasses[val] = [review[:-1].split()]
    return allClasses

def trainAndTest(allClasses):
    totalAmount = len(allClasses[0])
    trainAmount = round(0.8* totalAmount)
    
    testClasses =  {0:allClasses[0][trainAmount:totalAmount],1:allClasses[1][trainAmount:totalAmount]}
    trainClasses = {0:allClasses[0][0:trainAmount],1:allClasses[1][0:trainAmount]}
    
    return testClasses, trainClasses

def posDict(allClasses):
    words = list(chain.from_iterable(allClasses[1]))
    posClass = Counter(words)
    
#     posClass = {}
#     for line in allClasses[1]:
#         for word in line.split(): 
#             if word in posClass :
#                 posClass[word]+=1
    
#             else:
#                 posClass[word] = 1
    return(posClass)

def negDict(allClasses):
    words = list(chain.from_iterable(allClasses[0]))
    negClass = Counter(words)
    
#     negClass = {}
#     for line in allClasses[0]: 
#         for word in line.split(): 
#             if word in negClass :
#                 negClass[word]+=1
#             else:
#                 negClass[word] = 1
    return(negClass)
    
def logPrior(trainClasses):
    poslogPrior = np.log(len(trainClasses[0])
                         /(len(trainClasses[0])+len(trainClasses[1])))
    neglogPrior = np.log(len(trainClasses[1])/(len(trainClasses[0])+len(trainClasses[1])))
    
    return poslogPrior, neglogPrior
    
def totalDict(posDict, negDict):
    totalDict = posDict.copy()   # start with x's keys and values
    for key in negDict:
        if key in totalDict:
            totalDict[key] += negDict[key]
        else:
            totalDict[key] = negDict[key]
            
       
    return totalDict

def logLikelihood(denominator, Class, word):
    if word in Class.keys():
        numerator = Class[word] +1
    else:
        numerator = 1
    
    #denominator2= 0 
    #for item in totalDict.keys():
    #    if item in posClass.keys():
    #        denominator2+= 1 + posClass[item]
    #    else:
    #        denominator2+= 1
            
    #rint(denominator, "the loop one is")
    #rint(denominator2, "this is the non loop one")
   
    logLikelihoodPos =  np.log(numerator/denominator)
    return logLikelihood

def logLikelihoodDenominator(totalDict, negClass,posClass):
    denominator= len(set(totalDict.keys()) - set(Class.keys()))+len(Class.keys())
    denominator+= sum(Class.values())
    
    return denominator
    
def train(totalDict, posClass, negClass):
    likelihoodDict = {}
    for key in totalDict.keys():
        likelihoodDict[key]=(logLikelihoodPos(totalDict, posClass, key),logLikelihoodNeg(totalDict, negClass, key))
        
    return likelihoodDict

def test(testClasses):     
    percentCorrect = 0 
    total = 0
    
    for line in testClasses[0]:
        isPos = 0 
        isNeg = 0
        total+=1
        for word in line: 
            if word in likelihoodDict.keys():
                isPos +=likelihoodDict[word][0]
                isNeg +=likelihoodDict[word][1]
        if isNeg> isPos:
            percentCorrect+=1
            
    for line in testClasses[1]:
        isPos = 0 
        isNeg = 0
        total+=1
        for word in line: 
            if word in likelihoodDict.keys():
                isPos +=likelihoodDict[word][0]
                isNeg +=likelihoodDict[word][1]
        if isNeg< isPos:
            percentCorrect+=1
    accuracy = (percentCorrect/total)*100
    print("my accuracy is", accuracy, "woo hoo!")
    print("the total is", total)
    print("correct", percentCorrect)
                
allClasses = readToDict('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
trainClasses, testClasses = trainAndTest(allClasses)
posClass = posDict(trainClasses)
negClass = negDict(trainClasses)
totalDict = totalDict(posClass, negClass)
poslogPrior, neglogPrior = logPrior(trainClasses)
likelihoodDict  = train(totalDict, posClass, negClass)
test(testClasses)   
    

