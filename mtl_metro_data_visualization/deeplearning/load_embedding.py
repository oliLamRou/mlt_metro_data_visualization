import pandas as pd
import numpy as np
import ast

def str_to_numpy(string):
	return np.array(ast.literal_eval(string))

df = pd.read_csv('./temp.csv', converters={'embedding': str_to_numpy}).head()

x = df['embedding'].iloc[0]
print(type(x[0]))