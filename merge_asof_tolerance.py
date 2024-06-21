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
             
                Python Tip Friday: 06/21/2024
                  merge_asof time tolerance
    ----------------------------------------------------
    Stu Sztukowski | https://linkedin.com/in/StatsGuy
                   | https://github.com/stu-code
'''

''' Suppose you have a dataframe of times and and an indicator. You need
    to create groups of values based on that indicator. Whenever this
    indicator is 1 for an ID, you want to get every row that is at most
    10 days before. All other rows need to be dropped. For example, we want
    to convert this:
        
    id  datetime             indicator
    1   2020-01-14 00:12:00  0          
    1   2020-01-17 00:23:00  1          
    1   2020-01-17 00:13:00  0          
    1   2020-01-20 00:05:00  0          
    1   2020-05-19 00:00:00  0          
    1   2020-05-20 00:00:00  1          
    
    Into this:
        
    id  datetime             group      
    1   2020-01-14 00:12:00  A          
    1   2020-01-17 00:23:00  A          
    1   2020-01-17 00:13:00  A          
    1   2020-05-19 00:00:00  B          
    1   2020-05-20 00:00:00  B          
    
    Here's how you can do it with a little trick using merge_asof
'''
import pandas as pd
import numpy as np

data = {'id': [1,1,1,1,1,1,1],
        'datetime': ['2020-01-14 00:12:00', 
                     '2020-01-17 00:23:00',
                     '2020-01-17 00:13:00',
                     '2020-01-20 00:05:00',
                     '2020-03-10 00:07:00',
                     '2020-05-19 00:00:00',
                     '2020-05-20 00:00:00'],
        'ind': [0,1,0,0,0,0,1]
       }

df = pd.DataFrame(data)
df['datetime'] = df['datetime'].astype('datetime64[ns]')

# Step 1: Pull all dates where the indicator is 1
df['date'] = df['datetime'].dt.date.astype('datetime64[ns]')
df2 = df.loc[df['ind'] == 1, ['id', 'date', 'ind']].rename({'ind': 'ind2'}, axis=1)

# Step 2: Join them with merge_asof() with direction=forward and a tolerance of 10 days.
# This will join all data up to 10 days looking forward

df = pd.merge_asof(df.drop('ind', axis=1), 
                   df2, 
                   by='id', 
                   on='date', 
                   tolerance=pd.Timedelta('10d'), 
                   direction='forward'
                  )

# Step 3: Create groups. There are three rules we want to use:
#     1. The next value of ind2 is NaN
#     2. The next value of ID is not the current value of ID (we're at the last value in the group)
#     3. The next day is 10 days greater than the current
# With these rules, we can create a Boolean which we can then cumulatively 
# sum to create our groups.

df['group_id'] = df['ind2'].eq(  (df['ind2'].shift() == np.NaN) 
                               | (df['id'].shift() != df['id'])
                               | (df['date'] - df['date'].shift() > pd.Timedelta('10d') ) 
                              ).cumsum()

# Now drop all the NaNs, and we're done
df = df.dropna(subset='ind2').drop(['date', 'ind2'], axis=1)

print(df)
