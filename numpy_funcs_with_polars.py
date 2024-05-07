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
             
                Python Tip Friday: 05/10/2024
        Using numpy functions with Polars DataFrames
    ----------------------------------------------------
    Stu Sztukowski | https://linkedin.com/in/StatsGuy
                   | https://github.com/stu-code
'''

''' Polars supports numpy universal functions (ufuncs). Thanks to this
    feature, you can use many numpy functions within Polars as you
    would expect. This program includes an example of calculating an
    elasticity metric that uses the np.expm1() and np.log1p() functions
    in both Pandas and Polars, showing how similar the two calculations are
    to each other. Not much modification is needed to convert this from
    Pandas to Polars.
'''

import polars as pl
import pandas as pd
import numpy as np

# Polars DataFrame
pl_df = pl.DataFrame({"elasticity_intercept": [-6.195475, -8.437139, -4.741667],
                      "elasticity_coefficient": [1.553659, 2.048057, 1.285653],
                      "discount_price": [126, 129, 115],
                     })

# Pandas DataFrame
pd_df = pl_df.to_pandas()


# Calculate huber elasticity with pandas
pd_df["huber_elasticity"] = ( np.expm1(pd_df["elasticity_intercept"] + 
                                      pd_df["elasticity_coefficient"] *
                                      np.log1p(pd_df["discount_price"])
                                      )
                            )

# Calculate huber elasticity with polars
pl_df = pl_df.with_columns(np.expm1(pl.col('elasticity_intercept') + 
                                    pl.col('elasticity_coefficient') * 
                                    np.log1p(pl.col('discount_price') )
                                   )
                             .alias('huber_elasticity')
                          )

# Compare 
print('Pandas huber_elasticity')
print(pd_df['huber_elasticity'])

print('\n')

print('Polars huber_elasticity')
print(pl_df['huber_elasticity'])
