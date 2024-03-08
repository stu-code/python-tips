'''
                         ,/(/*.                 
                   (((((((((((((((((            
                  /((   (((((((((((##           
                  /(((((((((((((#####           
             ,/////////(/(((((####### .....     
          ((((((((((((((((((######### ........  
         (((((((((((((((((########### ........  
        .(((((((((((((((###########* .......... 
        /((((((((((*             .............. 
         ((((((((( ............................ 
         (((((((( ............................  
           (((((#  ........................,.   
                  ...................           
                  ..............  ...           
                   ............   .,,           
                     ..,..........     
             
                Python Tip Friday: 03/08/2024
            Choosing the best XGboost iteration
    ----------------------------------------------------
    Stu Sztukowski | https://linkedin.com/in/StatsGuy
                   | https://github.com/stu-code
'''

''' It is important to always split your data into training and
    validation dataframes. If you run XGBoost on the entire dataset,
    and tell it to fit as best as possible, it may overfit. Instead,
    get the best fit for your training dataset, compare it against
    the validation datafrane, and stop when it starts to degrade. This
    is the best stopping point for your model. Once you do find the
    stopping point, run it against your entire dataframe only with 
    that number of iterations. This example will use the classic
    HMEQ dataset for predicting bad loans.
'''

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

###################################################
#################### Data Prep ####################
###################################################

# Read data
df_hmeq = pd.read_csv('https://raw.githubusercontent.com/stu-code/python-tips/main/data/hmeq.csv')

# Create X and y matrices, then split into train/test (AKA validation) dataframes.
# We're going to drop categoricals to prevent one-hot encoding just for simplicity.
X = df_hmeq.drop(['BAD', 'JOB', 'REASON'], axis=1)
y = df_hmeq['BAD']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

###################################################
################## Train and Fit ##################
###################################################

# Train the model and stop when it overfits. We'll go through up to 1000
# boosting rounds, but stop if it starts to overfit after 20 rounds
xgb_model = xgb.XGBClassifier(objective="binary:logistic", 
                              random_state=101, 
                              early_stopping_rounds=20,
                              n_estimators=1000,
                             )

xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

print(f'The best number of iterations is {xgb_model.best_iteration}')

# Fit with full data but stop on the best iteration using xgb_model.best_iteration
xgb_model = xgb.XGBClassifier(objective="binary:logistic", 
                              random_state=101, 
                              n_estimators=xgb_model.best_iteration # <- Very helpful
                             )
xgb_model.fit(X, y)

###################################################
##################### Evaluate ####################
###################################################

# Now we can take a look at our model with a classification matrix and report
y_pred = xgb_model.predict(X_test)

print('\nConfusion Matrix')
print(confusion_matrix(y_test, y_pred))
print('\nClassification Report')
print(classification_report(y_test, y_pred))