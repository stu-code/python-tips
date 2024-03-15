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
             
                Python Tip Friday: 03/15/2024
             Using SQL to join Pandas DataFrames
    ----------------------------------------------------
    Stu Sztukowski | https://linkedin.com/in/StatsGuy
                   | https://github.com/stu-code
'''

''' There are a number of options available to work with DataFrames. 
    One of these is through SQL thanks to pandasql. In this case, we
    want to join two tables together and fill in blank rows. In the tables
    below, SID is missing from df1 but is available in df2. df1 and df2 
    can be joined by PID = SID. You can do this with a pd.merge, drop old 
    values and rename them. Or, you can use SQL. Either option will 
    produce the same answer. Remember: Use what's comfortable for YOU!
    That is the beauty of having options.
'''

import pandas as pd
import pandasql as pdsql
import numpy as np

# Create sample data 
df1 = pd.DataFrame({'Name': ['Alex', 'Oak', 'niva', 'mark'],
                    'ID':   ['A1', 'A2', 'A3', 'A4'],
                    'Course': ['Under', 'Under', 'grad', 'Under'],
                    'SID': ['', '', '', ''],
                    'Subject': ['chemistry', 'chemistry', 'physics', 'med']}
                   )

df2 = pd.DataFrame({'PID': ['A1', 'A2', 'A3'],
                    'ServiceId': ['WI', 'MI', 'OH'],
                    'Address': ['WI', 'MI', 'OH'],
                    'Active': ['Yes', 'Yes', 'Yes']}
                  )

#####################################
########## PandaSQL Method ##########
#####################################

# Create our query for joining DF1 with DF2 and filling in DF2's value of
# ServiceID
query = '''

SELECT df1.Name, 
       df1.ID, 
       df1.Course,  
       df1.Subject,
       df2.ServiceId as SID
FROM df1
LEFT JOIN
     df2
ON df1.ID = df2.PID

'''

# Run the query
df_want = pdsql.sqldf(query)

#####################################
######## Pure Pandas method #########
#####################################

df_want2 = ( df1.merge(df2, left_on="ID", right_on="PID", how='left')
                .drop(['SID', 'PID', 'Address', 'Active'], axis=1)
                .replace({np.nan: None})
                .rename(columns={'ServiceId':'SID'})
           )

print('pandasql method\n')
print(df_want)

print('\n-----------------------------------------------\n')

print('Pure pandas method\n')
print(df_want2)
