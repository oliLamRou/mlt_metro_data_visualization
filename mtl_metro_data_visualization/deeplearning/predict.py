import pandas as pd
import numpy as np
import ast
import tensorflow as tf
import keras

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
train, val, test = np.split(df_.sample(frac=1), [int(0.7*len(df_)), int(0.85*len(df_))])
val_data = df_to_dataset(val)

model = keras.saving.load_model('../../model/stop.keras')


predictions = model.predict(val_data)
# print(predictions)

val_stop = val.stop.to_list()
val_tweet = val.tweet.to_list()
for i in range(predictions.shape[0]):
	pred = 0 if predictions[i][0] < 0.97 else 1
	if val_stop[i] != pred:
		print(predictions[i][0], val_stop[i], val_tweet[i])
	

# preds = [np.argmax(p) for p in predictions]

