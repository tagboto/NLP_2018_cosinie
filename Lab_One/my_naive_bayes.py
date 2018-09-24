
# coding: utf-8

# # Natural Language Processing Assignment 1
# ## My Naive Bayes Classifier 
# 
# Name: Zoe Tagboto
# 
# 

# In[71]:

import numpy as np
import re
from collections import Counter
from itertools import chain
import random
import string
import sys


# <i> Below we define a function gathers the reviews from the file, cleans each line, and puts them in a dictionary based on the class of each review </i>

# In[]:

def read_file_to_dict(*filenames):
    all_classes = {}
    for filename in filenames:
        for line in open(filename):
            #These lines are to clean my data
            clean_line = re.sub(r"[""\n\t!'';:&*():?%$#+]","",line.lower())
            clean2 = re.sub(r"[/,.-]"," ",clean_line)
            val = int(clean2[-1][-1])
            review = re.sub(r"[0-9]+","",clean2[:-1])

            #once I clean I add my items to a dictionary based on their label value
            if val in all_classes:
                all_classes[val].append(review.split())
            else:
                all_classes[val] = [review.split()]
   
    #I then return the dictionary of reviews
    return all_classes


# <i>Below we define the function to split our data into test and training sets</i>

# In[]:

def split_train_and_test(all_classes):
    #first I shuffle the data and then I split them into train and test classes
    np.random.shuffle(all_classes[0])
    np.random.shuffle(all_classes[1])
    total_amount = len(all_classes[0])
    train_amount = round(0.2* total_amount)
    
    test_classes =  {0:all_classes[0][train_amount:total_amount],1:all_classes[1][train_amount:total_amount]}
    train_classes = {0:all_classes[0][0:train_amount],1:all_classes[1][0:train_amount]}
    
    return test_classes, train_classes
                                                


# <i> Here we define a function that creates a dictionary for each class that contains each word in the class and how often they are used </i>

# In[]:

def class_dict(all_classes, index):
    #This creates a dictionary of all words given a class and their counds
    words = list(chain.from_iterable(all_classes[index]))
    type_class = Counter(words)

    return(type_class)


# <i> Here we calculate the log prior which uses the following equation </i>
# 
# $$\log \frac{N_c}{N_{doc}}$$

# In[]:

def log_prior(train_classes):
    pos_log_prior = np.log(len(train_classes[0])
                         /(len(train_classes[0])+len(train_classes[1])))
    neg_log_prior = np.log(len(train_classes[1])/(len(train_classes[0])+len(train_classes[1])))
    
    return pos_log_prior, neg_log_prior
    


# <i> Below we define a function that creates a dictionary with a count of every word that occurs in the file </i>

# In[]:

def complete_vocab_list(pos_dict, neg_dict):
    total_dict = pos_dict.copy()   # start with the pos_dicts's keys and values
    for key in neg_dict:
        if key in total_dict:       #then I add the neg_dict's keys and values if they aren't already in the file
            total_dict[key] += neg_dict[key]
        else:
            total_dict[key] = neg_dict[key]
            
       
    return total_dict 


# <i>Below we define the function to calculate the logLikelihood using the following equation:</i>
# $$\log \frac{count(w_{i}, c)+1}{\sum_{w\in v}^{}(count(w, c)+1)}$$
# 

# In[]:

def log_likelihood_class(total_dict,Class, word):
    if word in Class.keys():
        numerator = Class[word] +1
    else:
        numerator = 1   
    
    
    denominator= len(set(total_dict.keys()) - set(Class.keys()))+len(Class.keys())
    denominator+= sum(Class.values())
    
    log_likelihood =  np.log(numerator/denominator)
    
    
    
    return log_likelihood



# <i>Below we calculate the positive and negative likelihood for each word in the training set. We then return a dictionary that has the word as a value and a tuple containing negative and positive reviews</i>
# 
# For example {good:(-7, -2)}

# In[]:

def train(total_dict, pos_class, neg_class):
    likelihood_dict = {}
    for key in total_dict.keys():
        likelihood_dict[key]=(log_likelihood_class(total_dict,neg_class, key),log_likelihood_class(total_dict,pos_class, key))
        
    return likelihood_dict  


# In[ ]:

# <i> This was a test file so I could check my own accuracy </i>


# In[]:

def test(test_classes, likelihood_dict):     
    number_correct = 0 
    total = 0
    
    for line in test_classes[0]:
        is_pos = 0 
        is_neg = 0
        total+=1
        for word in line: 
            if word in likelihood_dict.keys():
                is_pos +=likelihood_dict[word][1]
                is_neg +=likelihood_dict[word][0]
        if is_neg> is_pos:
            number_correct+=1
            
    for line in test_classes[1]:
        is_pos = 0 
        is_neg = 0
        total+=1
        for word in line: 
            if word in likelihood_dict.keys():
                is_pos +=likelihood_dict[word][1]
                is_neg +=likelihood_dict[word][0]
    
        if is_neg< is_pos:
            number_correct+=1
    
    accuracy = (number_correct/total)*100
    print("my accuracy is", accuracy, "woo hoo!")
    print("the total tested were", total)
    print("the number we got correct were", number_correct)
 
                
    
    


# <i> This is my test function that will test data from unknown file provided by the professor </i>

# In[]:

def test_main(name_of_file,likelihood_dict):
    results= open("results.txt","w+")
    for line in open(name_of_file):
            #print(type(line))
            clean_line = re.sub(r"[""\n\t!'';:&*():?%$#+]","",line.lower())
            #print(type(clean_line))
            clean_2 = re.sub(r"[/,.-]"," ",clean_line)
            #print(type(review))
            review = re.sub(r"[0-9]+","",clean_2)

            review2 = review.split()
            
            for word in review2: 
                is_pos = 0 
                is_neg =0
                if word in likelihood_dict.keys():
                    is_pos +=likelihood_dict[word][1]
                    is_neg +=likelihood_dict[word][0]
            
            if is_neg> is_pos:
                # create document and add 0 to end of sentence
                results.write("0\n")
                
            elif is_pos>is_neg:
                # create document and add 1 to the end of sentence 
                results.write("1\n")
                
            else:
                results.write("The classifier was unable to determine the sentiment of this file\n")
            
            
            
            
    
    


# <i> Didn't end up using this but in theory I could improve accuracy by removing stop words </i>

# In[]:

def remove_stop_words(allClasses):
    stopList = ['a','about','above','after','again',' all', 'am','an','and','any','are','as','at','az','b','be','because', 
                'been','before','being','bethe','between','both','but','by','bt','do','does','doing','down','during','each',
                'few','for','from','further','had','has','have''having','he','hed','hell','hes','her','here',
                'heres','hers','herself','him','himself','his','how','hows','i','id','ill','im','ive''ir','if',
                'in','into','is','it','its','lets','me','more','my','myself','of','on','once','only','or','other',
                'ought', 'our','ours','ourselves','out','over','own','same','she','shed','shell','shes','should',
                'so','some','such','than','that','thats','the','their','theirs','them','themselves','then','there',
                'theres','these','they','theyd','theyll','theyre','theyve','this','those','through','to','too','under',
                'until','up','very','was','we','wed','well','were','weve','were','what','whats','when','whens','where',
                'wheres','which','while','who','whos','whom','why','whys','with','would','you','youd','youll','youre',
                'youve','your','yours','yourself','yourselves']
    



# <i> This the function that does all the work. It calls all my mini functions and ties everything together</i>

# In[ ]:

def run_file(name_of_file):
    all_classes = read_file_to_dict('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    train_classes, test_classes = split_train_and_test(all_classes)
    pos_class = class_dict(train_classes,1)
    neg_class = class_dict(train_classes,0)
    total_dict = complete_vocab_list(pos_class, neg_class)
    pos_log_prior, neg_log_prior = log_prior(train_classes)
    likelihood_dict  = train(total_dict, pos_class, neg_class)
    test(test_classes,likelihood_dict)
    test_main(name_of_file,likelihood_dict)
    
    


# <i>This is the main function where you can call everything via the command line</i>

# In[]:

def main():
    script = sys.argv[0]
    file_name = sys.argv[1]
    run_file(file_name)


# In[ ]:

main()

