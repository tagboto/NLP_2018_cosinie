
# coding: utf-8

# In[29]:

import sys
from my_naive_bayes_2 import normalized_NB, unnormalized_NB
from my_logistic_regression import normalized_LR, unnormalized_LR



# In[36]:


def main():    
    classifier_type =sys.argv[1]
    norm_or_un = sys.argv[2]
    file = sys.argv[3]
    
       
    if classifier_type == "nb" and norm_or_un == "u":
        print("you are running the unnormalized naive bayes classifier")
        predicions  = unnormalized_NB(file)
    elif classifier_type == "nb" and norm_or_un == "n":
        print("you are running the normalized naive bayes classifier") 
        predictions = normalized_NB(file)
    elif classifier_type == "lr" and norm_or_un == "n":
        print("you are running the normalized logistic regression classifier")
        predictions = normalized_LR(file)
    elif classifier_type == "lr" and norm_or_un == "u":
         print("you are running the unnormalized logistic regression classifier")
         predictions = unnormalized_LR(file)
    else:
        print("You have made an error. Please try again")
        
        sys.exit()
        
    
    


# In[38]:


main()

