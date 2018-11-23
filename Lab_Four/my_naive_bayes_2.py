
# coding: utf-8

# # Natural Language Processing 
# 
# ## Assignment 4
# 
# ### My Naive Bayes Classifier 2
# 
# ### Name: Zoe Tagboto
#  

# A list of all the libraries used to make my classifier

# In[84]:


import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.metrics import accuracy_score, classification_report


# <i> Below we define a function gathers the reviews from the file, cleans each line, and puts them into two lists based on the class of each review </i>

# In[95]:


def read_file_to_list_cleaned(*filenames):
    labels =[]
    reviews =[]
    all_classes = {}
    for filename in filenames:
        for line in open(filename):
            r2 = re.compile(r'[^a-zA-Z0-9]', re.MULTILINE)
            s = r2.sub(' ', line)
            #newS = s.lower()
            val = int(s[-2])
            
            labels.append(val)
            reviews.append(s[:-2])
            
    return reviews, labels


# <i> Below we define a function gathers the reviews from the file, without cleaning each line, and puts them in two lists based on the class of each review </i>

# In[96]:


def read_file_to_list_uncleaned(*filenames):
    labels =[]
    reviews = []
    for filename in filenames:
        for line in open(filename): 
            val = int(line[-2])
            
            reviews.append(line.lower()[:-2])
            
            labels.append(val)
            
    return reviews, labels


# In[108]:


def nb_train(reviews,labels, Boolean):

    #N-gram model that comes up with features or occurances of words
    if Boolean == True:
        count_vect = CountVectorizer(stop_words='english')
        
    else:
        count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(r for r in reviews)
    
    # This is to scale down impact of tkens that occur very frequently and arent
    #very informative.
    #Term Frequency time Inverse Document Frequency
    
    tf_transform = TfidfTransformer()
    X_train_tf = tf_transform.fit_transform(X_train_counts)
    
    #splitting data into test and training sets
    X_train, X_test, Y_train, Y_test =train_test_split(X_train_tf,labels, random_state = 35 , train_size =0.90, test_size =0.10)
 

    #MAKING THE MODEL
    nb = MultinomialNB()
    model = nb.fit(X_train, Y_train)
    #array.reshape(-1, 1)
    
    return nb, tf_transform, count_vect, model, X_test, Y_test
    
  


# In[109]:


def nb_test(test_file,reviews,labels, Boolean):
   nb,tf_transform, count_vect, model, X_test, Y_test = nb_train(reviews,labels, Boolean)
  
 
   
   #Now using the test set I need to know if I'm right
   test_data = []
   for line in open(test_file):
       r2 = re.compile(r'[^a-zA-Z0-9]', re.MULTILINE)
       s = r2.sub(' ', line)
       test_data.append(s)
   test_data = stemming(test_data)
   test_data = lemming(test_data)
   
   
   
   #Making sentiment classification
   for i in range (len(test_data)):
       X_pred_counts = count_vect.transform(test_data)
       X_pred_tf = tf_transform.transform(X_pred_counts)
       predictions = nb.predict(X_pred_tf)
               
                       
   #Evaluating the model using the classification report function form sklearn

   predicted = model.predict(X_test)    
   print("The accuracy of this testis: " ,accuracy_score(Y_test, predicted)*100) 

   print("This is a more detailed report of the classifiers performance: \n" ,classification_report(Y_test, predicted))
   
   return(predictions,"\n")                                                
                                                    
                                       


# In[64]:


def stemming(reviews):
    lancaster_stemmer = LancasterStemmer()
    n_reviews = []
    for review in reviews:
        n_reviews.append(' '.join(lancaster_stemmer.stem(token)for token in nltk.word_tokenize(review)))
    return(n_reviews)


# In[65]:


def lemming(reviews):
    wordnet_lemmatizer = WordNetLemmatizer()
    n_reviews = []
    for review in reviews:
        n_reviews.append(' '.join(wordnet_lemmatizer.lemmatize(token)for token in nltk.word_tokenize(review)))
    return(n_reviews)


# In[66]:


def write_cleaned_data():
    reviews, labels = read_file_to_list_cleaned('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    reviews = stemming(reviews)
    reviews = lemming(reviews)

    predictions = naiveBayes(reviews,labels,'test_sentences2.txt')
    

    # write to file to gage my accuracy
    with open("normalized_results.txt", "w+") as file:
        file.write(str(predictions))


# In[112]:


def normalized_NB(file):
    reviews, labels = read_file_to_list_cleaned('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    reviews = stemming(reviews)
    reviews = lemming(reviews)
    predictions = nb_test(file,reviews, labels,True)
    write_results("nb", "n", predictions)


# In[113]:


#normalized_NB()


# In[110]:


def unnormalized_NB(file):
    reviews, labels = read_file_to_list_uncleaned('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    #print(reviews,labels)
    predictions = nb_test(file,reviews, labels, False)
    write_results("nb", "u", predictions)
    return predictions
    
def write_results(classifier_type, norm_or_un, predictions): 
    with open(classifier_type+"_"+norm_or_un+"_"+"results.txt", "w+") as file:
        for label in predictions[0]:
            file.write(str(label)+"\n")
# In[111]:


#unnormalized_NB()

