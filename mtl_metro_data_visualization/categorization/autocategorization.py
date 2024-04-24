import ast
import pandas as pd
import tensorflow as tf
import keras

from mtl_metro_data_visualization.constant.path import TRAINING_DATA_PATH
from mtl_metro_data_visualization.categorization.training_data import TrainingData

class Autocategorization:

    """docstring for Autocategorization"""
    def __init__(self):
        self._model = None

        self._train_data = None
        self._test_data = None
        self._val_data = None
        self._val_data_df = None

    @property
    def train_data(self):
        if self._train_data == None:
            self._train_data = self.load_csv_option('train_data.csv')
            self._train_data = self.df_to_dataset(self._train_data)

        return self._train_data

    @property
    def test_data(self):
        if self._test_data == None:
            self._test_data = self.load_csv_option('test_data.csv')
            self._test_data = self.df_to_dataset(self._test_data)

        return self._test_data

    @property
    def val_data(self):
        if self._val_data == None:
            self._val_data_df = self.load_csv_option('val_data.csv')
            self._val_data = self.df_to_dataset(self._val_data_df)

        return self._val_data

    @property
    def model(self):
        if self._model == None:
            self._model = tf.keras.Sequential()
            self._model.add(tf.keras.layers.Dense(128, activation='relu'))
            self._model.add(tf.keras.layers.Dropout(0.01))
            self._model.add(tf.keras.layers.Dense(64, activation='relu'))
            self._model.add(tf.keras.layers.Dropout(0.01))
            self._model.add(tf.keras.layers.Dense(32, activation='relu'))
            self._model.add(tf.keras.layers.Dropout(0.01))
            self._model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

            self._model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss=tf.keras.losses.BinaryCrossentropy(),
                metrics=['accuracy']
            )    

        return self._model

    def load_csv_option(self, filename):
        return pd.read_csv(TRAINING_DATA_PATH + filename, converters={'embedding': self.str_to_numpy})

    def str_to_numpy(self, string):
        return (ast.literal_eval(string))

    def df_to_dataset(self, dataframe, shuffle=True, batch_size=32):
        df = dataframe.copy()
        labels = df.pop('stop')
        df = df['embedding'].to_list()
        ds = tf.data.Dataset.from_tensor_slices((df, labels))
        
        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))

        ds = ds.batch(batch_size)
        ds = ds.prefetch(tf.data.AUTOTUNE)
        
        return ds

    def training(self, epochs):
        history = self.model.fit(self.train_data, epochs=epochs, validation_data=self.test_data)
        self.model.save('../../model/stop.keras')

    def validation(self):
        predictions = self.model.predict(self.val_data)

        val_stop = self._val_data_df.stop.to_list()
        val_tweet = self._val_data_df.tweet.to_list()
        for i in range(predictions.shape[0]):
            pred = 0 if predictions[i][0] < 0.97 else 1
            if val_stop[i] != pred:
                print(predictions[i][0], val_stop[i], val_tweet[i])

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
    a.predict('something')