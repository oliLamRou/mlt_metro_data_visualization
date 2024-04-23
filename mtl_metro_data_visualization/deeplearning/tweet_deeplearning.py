import os
import string
import re

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from mtl_metro_data_visualization.categorization.tweet import Tweet

os.environ["KERAS_BACKEND"] = "tensorflow"

import keras
import tensorflow as tf
import tensorflow_hub as hub

from keras import layers


df_ = pd.read_csv('./temp.csv')

# path = '../../data/twitter_stm_rem.csv'
# tweet = Tweet(path)
# tweet.load_preprocess
# df_ = tweet.df_.copy()

train, val, test = np.split(df_.sample(frac=1), [int(0.7*len(df_)), int(0.85*len(df_))])

x = train['embedding'].values[0]



# X_train = tf.convert_to_tensor(train.embedding)
# y_train = tf.convert_to_tensor(train.stop)
# X_test = tf.convert_to_tensor(test.embedding)
# y_test = tf.convert_to_tensor(test.stop)
# X_val = tf.convert_to_tensor(val.embedding)
# y_val = tf.convert_to_tensor(val.stop)

# print(X_train[0])

# def df_to_dataset(dataframe, shuffle=True, batch_size=32):
# 	df = dataframe.copy()
# 	labels = df.pop('stop')
# 	df = df['tweet']
# 	ds = tf.data.Dataset.from_tensor_slices((df, labels))
	
# 	if shuffle:
# 		ds = ds.shuffle(buffer_size=len(dataframe))

# 	ds = ds.batch(batch_size)
# 	ds = ds.prefetch(tf.data.AUTOTUNE)
	
# 	return ds

# train_data = df_to_dataset(train)
# # print(list(train_data)[0][0])

# test_data = df_to_dataset(test)
# val_data = df_to_dataset(val)


# embedding = "https://www.kaggle.com/models/google/nnlm/TensorFlow2/en-dim50/1"
# hub_layer = hub.KerasLayer(embedding, dtype=tf.string, trainable=True)

# model = tf.keras.Sequential()
# model.add(tf.keras.layers.Dense(16, activation='relu', input_shape=()))
# model.add(tf.keras.layers.Dense(16, activation='relu'))
# model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
# 			loss=tf.keras.losses.BinaryCrossentropy(),
# 			metrics=['accuracy'])

# model.evaluate(list(train_data)[0][0])