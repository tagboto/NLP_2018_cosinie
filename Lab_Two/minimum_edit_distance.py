
# coding: utf-8

# # Natural Language Processing Assignment 2
# ## Minimum Edit Distance
# 
# Name: Zoe Tagboto

# In[28]:


import numpy as np


# In[29]:


def min_edit_distance(source_word, target_word):  
    # First I find the length of my words and create a matrix
    source_word_len = len(source_word)
    target_word_len = len(target_word)
    matrix = np.zeros ((source_word_len+1, target_word_len+1),np.int64)
    
    #These are the costs associated with deletion insertion 
    #and substitution
    
    del_cost = 1
    ins_cost = 1
    sub_cost = 2
    
    for x in range(source_word_len+1):
        matrix [x, 0] = x
        
    for y in range(target_word_len+1):
        matrix [0, y] = y
        
    #This is to compute the minimum edit distance
    for x in range(1, source_word_len+1):
        for y in range(1, target_word_len+1):
            if source_word[x-1] == target_word[y-1]:
                matrix [x,y] =  matrix[x-1, y-1]
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + del_cost,
                    matrix[x,y-1] + ins_cost,
                    matrix[x-1,y-1] + sub_cost)
            
            
                

    print ("The minimum edit distance between "+source_word+" and the "+target_word+" is " + 
        str(matrix[source_word_len, target_word_len]))


# In[30]:


min_edit_distance("intention", "execution")

