import re

def readFile(filename):
    reviews = []
    for line in open(filename):
        reviews.append(re.sub(r"[\n\t.!,'-()]*","",line.lower()))
    #reviews = [line.rstrip('\n/t') for line in open(filename)]
    return reviews

def splitData(reviews):
    allClasses = {}
    total = len(reviews)

    #split into dictionaries based on classses
    for review in reviews:
        val = int(review.split()[-1][-1])
        if val in allClasses:
            allClasses[val].append(review)
    
        else:
            allClasses[val] = [review]

    #now find probability of each class
    negProb = len(allClasses[0])/total
    posProb = len(allClasses[1])/total

    #return the split list and the negative and positive probability
    return(allClasses,negProb,posProb)



first = readFile('amazon_cells_labelled.txt')
splitClasses, negProb, posProb = splitData(first)
print(negProb, posProb)
