import pandas as pd
import numpy as np

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding

oh = OneHotEncoding()
print(oh.df[['date', 'stop']])

df = pd.read_csv('~/Downloads/stm_interruption.csv')
print(df.info())
# print(df["Cause primaire"].unique())

# print(df[['Jour calendaire', "Heure de l'incident", 'Incident en minutes']])
print(df["KFS"].unique())

#get same range
#sum stop (and slow) daily
#Filter out 10 or less event
#compare by getting difference
#scatter day of the year vs year with size = difference
#Get a statistical comparison

