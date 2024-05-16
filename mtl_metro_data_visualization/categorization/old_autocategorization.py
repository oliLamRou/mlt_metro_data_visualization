import ast
import pandas as pd
import numpy as np
import tensorflow as tf
import keras

from mtl_metro_data_visualization.constant.path import TRAINING_DATA_PATH
from mtl_metro_data_visualization.categorization.training_data import TrainingData

class Autocategorization:

    """docstring for Autocategorization"""
    def __init__(self):
        self._model = None

        self._train_data_tf = None
        self._test_data_tf = None
        self._val_data_tf = None

        self.training_data = TrainingData()
        self.training_data.build()

    @property
    def train_data_tf(self):
        if self._train_data_tf == None:
            self._train_data_tf = self.df_to_dataset(self.training_data.train_data)

        return self._train_data_tf

    @property
    def test_data_tf(self):
        if self._test_data_tf == None:
            self._test_data_tf = self.df_to_dataset(self.training_data.test_data)

        return self._test_data_tf

    @property
    def val_data_tf(self):
        if self._val_data_tf == None:
            self._val_data_tf = self.df_to_dataset(self.training_data.val_data)

        return self._val_data_tf

    @property
    def model(self):
        if self._model == None:
            self._model = tf.keras.Sequential()
            self._model.add(tf.keras.layers.Embedding(2569, 16))
            self._model.add(tf.keras.layers.Dense(16, activation='relu'))
            self._model.add(tf.keras.layers.Dropout(0.01))
            self._model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

            self._model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss=tf.keras.losses.BinaryCrossentropy(),
                metrics=['accuracy']
            )    # loss=tf.keras.losses.BinaryCrossentropy(),

        return self._model

    def df_to_dataset(self, dataframe, shuffle=True, batch_size=32):
        df = dataframe.copy()
        labels = df.pop('stop')
        df = df['embedding'].to_list()
        ds = tf.data.Dataset.from_tensor_slices((df, labels))
        print(ds)
        
        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))

        ds = ds.batch(batch_size)
        ds = ds.prefetch(tf.data.AUTOTUNE)
        
        return ds

    def training(self, epochs):
        history = self.model.fit(self.train_data_tf, epochs=epochs)#validation_data=self.test_data
        self.model.save('../../model/stop.keras')

    def validation(self):
        predictions = self.model.predict(self.test_data_tf)

        test_stop = self.training_data.test_data.stop.to_list()
        test_tweet = self.training_data.test_data.tweet.to_list()
        good = 0
        bad = 0
        for i in range(predictions.shape[0]):
            pred = 0 if predictions[i][0] < 0.97 else 1
            if test_stop[i] == pred:
                good += 1
            else:
                bad += 1

        print(f'good: {good}, bad: {bad}')
                # print(predictions[i][0], val_stop[i], val_tweet[i])

    def predict(self, string):
        tweet = 'something'
        loaded_model = keras.saving.load_model('../../model/stop.keras')
        embedding = TrainingData().sentence_to_vec(tweet)
        print(loaded_model.predict(embedding))

    def build(self):
        self.training(10)
        self.validation()

if __name__ == '__main__':
    a = Autocategorization()
    # a.build()
    print(a.train_data_tf)

    # a.predict('something')