
# coding: utf-8

# # Natural Language Processing 
# 
# ## Assignment 4
# 
# ### My Logistic Regression Classifier
# 
# ### Name: Zoe Tagboto

# In[7]:


import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.metrics import accuracy_score, classification_report


# In[8]:


def read_file_to_list_cleaned(*filenames):
    labels =[]
    reviews =[]
    all_classes = {}
    for filename in filenames:
        for line in open(filename):
            r2 = re.compile(r'[^a-zA-Z0-9]', re.MULTILINE)
            s = r2.sub(' ', line)
            val = int(s[-2])
            
            labels.append(val)
            reviews.append(s[:-2])
            
    return reviews, labels


# In[9]:


def read_file_to_list_uncleaned(*filenames):
    labels =[]
    reviews = []
    for filename in filenames:
        for line in open(filename): 
            val = int(line[-2])
            
            reviews.append(line.lower()[:-2])
            
            labels.append(val)
            
    return reviews, labels


# In[27]:


def lr_train(reviews,labels, Boolean):

    #N-gram model that comes up with features or occurances of words
    if Boolean == True:
        count_vect = CountVectorizer(stop_words='english')
        tf_transform = TfidfTransformer()
    else:
        count_vect = CountVectorizer( strip_accents=None, lowercase=False)
        tf_transform = TfidfTransformer(use_idf=False)
    X_train_counts = count_vect.fit_transform(r for r in reviews)
    
    # This is to scale down impact of tkens that occur very frequently and arent
    #very informative.
    #Term Frequency time Inverse Document Frequency

    X_train_counts = count_vect.fit_transform(r for r in reviews)
    
    # This is to scale down impact of tkens that occur very frequently and arent
    #very informative.
    #Term Frequency time Inverse Document Frequency
    
    X_train_tf = tf_transform.fit_transform(X_train_counts)
    
    #splitting data into test and training sets
    X_train, X_test, Y_train, Y_test =train_test_split(X_train_tf,labels, random_state = 35 , train_size =0.90, test_size =0.10)
 

    #MAKING THE MODEL
    lrn = LogisticRegression()
    model = lrn.fit(X_train, Y_train)
    #array.reshape(-1, 1)
    
    return lrn, tf_transform, count_vect, model, X_test, Y_test
    
  


# In[11]:


def lr_test(test_file,reviews,labels, Boolean):
   lrn,tf_transform, count_vect, model, X_test, Y_test = lr_train(reviews,labels, Boolean)
  
 
   
   #Now using the test set I need to know if I'm right
   test_data = []
   for line in open(test_file):
       r2 = re.compile(r'[^a-zA-Z0-9]', re.MULTILINE)
       s = r2.sub(' ', line)
       test_data.append(s)
   
   if Boolean == True:
       test_data = stemming(test_data)
       test_data = lemming(test_data)
       
   else:
       test_data = test_data
   
   
   
   #Making sentiment classification
   for i in range (len(test_data)):
       X_pred_counts = count_vect.transform(test_data)
       X_pred_tf = tf_transform.transform(X_pred_counts)
       predictions = lrn.predict(X_pred_tf)
               
                       
   #Evaluating the model using the classification report function form sklearn

   predicted = model.predict(X_test)    
   print("The accuracy of this test is: " ,accuracy_score(Y_test, predicted)*100) 

   print("This is a more detailed report of the classifiers performance: \n" ,classification_report(Y_test, predicted))
   
   return(predictions,"\n")                                                
                                                    
                                       


# In[12]:


def stemming(reviews):
    lancaster_stemmer = LancasterStemmer()
    n_reviews = []
    for review in reviews:
        n_reviews.append(' '.join(lancaster_stemmer.stem(token)for token in nltk.word_tokenize(review)))
    return(n_reviews)


# In[13]:


def lemming(reviews):
    wordnet_lemmatizer = WordNetLemmatizer()
    n_reviews = []
    for review in reviews:
        n_reviews.append(' '.join(wordnet_lemmatizer.lemmatize(token)for token in nltk.word_tokenize(review)))
    return(n_reviews)


# In[15]:


def normalized_LR(file):
    reviews, labels = read_file_to_list_cleaned('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    reviews = stemming(reviews)
    reviews = lemming(reviews)
    predictions = lr_test(file,reviews, labels,True)
    write_results("lr", "n", predictions)
    return predictions


# In[14]:


def write_results(classifier_type, norm_or_un, predictions): 
    with open(classifier_type+"_"+norm_or_un+"_"+"results.txt", "w+") as file:
        for label in predictions[0]:
            file.write(str(label)+"\n")


# In[23]:


#normalized_LR()


# In[17]:


def unnormalized_LR(file):
    reviews, labels = read_file_to_list_uncleaned('amazon_cells_labelled.txt', 'imdb_labelled.txt','yelp_labelled.txt')
    #print(reviews,labels)
    predictions = lr_test(file,reviews, labels, False)
    write_results("lr", "u", predictions)
    return predictions
    


# In[28]:





# In[ ]:



# In[ ]:



    
    

