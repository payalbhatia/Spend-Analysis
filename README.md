## Spend-Analysis
This is part of Experimentation 
# Problem :
Creating machine learning models using NLP& text analysis which can absorb information (inputs) from PO and Invoice line
descriptions, supplier names, GL codes, and other data to predict an appropriate spend category (output).  With NLP as part of an
enterprise's overall spend analytics solution, companies gain new insight into their spend. We can quickly see how much an organization
spending with a global vendor, even if purchases were made through diﬀerent channels, in diﬀerent locations. The organization will start to
see sizable cost reduction, as NLP identiﬁes and continues to improve its identiﬁcation of maverick spend and, see who is spending the
most, even identify areas of savings based on the analyses.

# Class of algorithm used And why :
The mentioned project is a classification problem. 
Used major classification algorithms Naive Bayes , KNN , Decision Tree , Random Forests , Boosting , 
and then stacking of those algorithms.
Since it was a multi class classification problem, we did not use any binary classification algorithms. 
Further ,  it has # imbalanced distribution. This means out of 7 categories , 2 categories have the major data. 
This was concerning.Part of the data in multiple languages. Though data was not that huge initially , so gave a shot to Naive Bayes. 
Then , for KNN it is a lazy algorithm.It was not giving a consistent result which was not helping. So , the random forest and stacked modelling came to rescue. Also, tried using SMOTE and other variations with data to check what algorithm works best.

# the accuracy metric :
Accuracy metric was not appropriate to our problem.Used confusion metrics. There also ,  focussed more on False positives for the categories. Also , the ROC-AUC score , which is independent of the threshold set for classification because it only considers the rank of each prediction and not its absolute value.

#  Prepare the data for this problem : 
Data was text data with multiple languages and a limited number of characters like twitter. Since it was a purchase description we do not have any grammatical or lemmatizing kind of data processing.Majorly clean the data by using regular expression. I read the data and used some API for language translation and checked patterns. Then created a function using regular expressions and part of it was done using excel. API cannot be utilized due to organization restrictions, tried available python libraries. Then created a bag of words and did tf idf process to create features.  Also, tried using stanford predefined models , but it was not relevant to our data. 

# The data used in reposirtory is a dummy data ; just to share the relevance of code 
