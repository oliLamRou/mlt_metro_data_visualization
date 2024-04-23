import os
import string
import re
import ast

import pandas as pd
import numpy as np

# os.environ["KERAS_BACKEND"] = "tensorflow"
import tensorflow as tf

# from mtl_metro_data_visualization.categorization.tweet import Tweet

def str_to_numpy(string):
	return (ast.literal_eval(string))#.astype('float16')

def df_to_dataset(dataframe, shuffle=True, batch_size=32):
	df = dataframe.copy()
	labels = df.pop('stop')
	df = df['embedding'].to_list()
	ds = tf.data.Dataset.from_tensor_slices((df, labels))
	
	if shuffle:
		ds = ds.shuffle(buffer_size=len(dataframe))

	ds = ds.batch(batch_size)
	ds = ds.prefetch(tf.data.AUTOTUNE)
	
	return ds

df_ = pd.read_csv('./temp.csv', converters={'embedding': str_to_numpy})#.head(3)
# path = '../../data/twitter_stm_rem.csv'
# tweet = Tweet(path)
# tweet.load_preprocess
# df_ = tweet.df_.copy()

train, val, test = np.split(df_.sample(frac=1), [int(0.7*len(df_)), int(0.85*len(df_))])
train_data = df_to_dataset(train)
test_data = df_to_dataset(test)
val_data = df_to_dataset(val)

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
			loss=tf.keras.losses.BinaryCrossentropy(),
			metrics=['accuracy'])

model.evaluate(list(train_data)[0][0], list(train_data)[0][1])

history = model.fit(train_data, epochs=3, validation_data=test_data)
model.save('../../model/stop.keras')

# model.predict(list(val_data)[0][0][0], list(val_data)[0][1][0])