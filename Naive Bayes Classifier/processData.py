import re

def readFile(filename):
    reviews = []
    for line in open(filename):
        cleanLine = re.sub(r"[\n\t!';:&():?%$#+]","",line.lower())
        reviews.append(re.sub(r"[/,.-]"," ",cleanLine.lower()))        
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
    print("number of neg reviews is",len(allClasses[0]))
    print("number of pos reviews is",len(allClasses[1]))
    print("number of total reviews is",total)
    
    return(allClasses,negProb,posProb)



first = readFile('imdb_labelled.txt')
splitClasses, negProb, posProb = splitData(first)
print(negProb, posProb)
