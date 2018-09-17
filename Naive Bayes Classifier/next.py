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
            
countP, posClass = posDict(allClasses)
countN, negClass = negDict(allClasses)
totalDict = totalDict(posClass, negClass)
