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
             
                Python Tip Friday: 03/29/2024
             Using SQL to join Polars DataFrames
    ----------------------------------------------------
    Stu Sztukowski | https://linkedin.com/in/StatsGuy
                   | https://github.com/stu-code
'''

''' There are a number of options available to work with DataFrames. 
    One of these is through SQL, which is built right in to Polars.
    Rather than needing to download a separate package like pandasql,
    you can execute SQL directly within polars. Here's an example of 
    merging two dataframes similarly to what we did in the 03/15/24 
    edition of Python Tip Friday. There's very little difference;
    you just don't need a separate package. Plus, polars is very
    efficient!
'''
import polars as pl

# Create sample data 
df1 = pl.DataFrame({'Name': ['Alex', 'Oak', 'niva', 'mark'],
                    'ID':   ['A1', 'A2', 'A3', 'A4'],
                    'Course': ['Under', 'Under', 'grad', 'Under'],
                    'SID': ['', '', '', ''],
                    'Subject': ['chemistry', 'chemistry', 'physics', 'med']}
                   )

df2 = pl.DataFrame({'PID': ['A1', 'A2', 'A3'],
                    'ServiceId': ['WI', 'MI', 'OH'],
                    'Address': ['WI', 'MI', 'OH'],
                    'Active': ['Yes', 'Yes', 'Yes']}
                  )

# Define the SQL context and register the two dataframes
ctx = pl.SQLContext().register_many({"df1": df1, "df2": df2})

# Create the query
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

# Execute and collect the results
df_merged = ctx.execute(query).collect()

print(df_merged)
