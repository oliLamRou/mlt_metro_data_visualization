import pandas as pd
import numpy as np 

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split

from mtl_metro_data_visualization.categorization.tweet import Tweet
from mtl_metro_data_visualization.constant.path import TRAINING_DATA_PATH

class TrainingData:
    EMBEDDING_MODEL_PATH = '../../model/french_semantic'

    def __init__(self):
        self._df = pd.DataFrame()

        self._embedding_model = None
        self.training_data = pd.DataFrame()

        self.train_data = pd.DataFrame()
        self.test_data = pd.DataFrame()
        self.val_data = pd.DataFrame()

    @property
    def df(self):
        if self._df.empty:
            self._df = Tweet().load_preprocess.copy()

        return self._df

    @property
    def embedding_model(self):
        if self._embedding_model == None:
            #NOTE: not sure if should load model everytime
            # model =  SentenceTransformer("Sahajtomar/french_semantic")
            # model.save(EMBEDDING_MODEL_PATH)
            self._embedding_model = SentenceTransformer(self.EMBEDDING_MODEL_PATH)

        return self._embedding_model

    def sentence_to_vec(self, sentence):
        return list(self.embedding_model.encode(sentence))

    def train_test_val_split(self):
        self.train_data, temp = train_test_split(self.training_data, test_size=0.25)
        self.test_data, self.val_data = train_test_split(temp, test_size=0.5)
        
    def process_embedding(self):
        #For now working only on tweet + stop
        self.training_data = self.df[['tweet', 'stop']].copy()
        self.training_data['embedding'] = self.df['tweet'].apply(self.sentence_to_vec)

        return self.training_data

    def save_training_data(self):
        self.train_data.to_csv(TRAINING_DATA_PATH + 'train_data.csv', index=False)
        self.test_data.to_csv(TRAINING_DATA_PATH  + 'test_data.csv', index=False)
        self.val_data.to_csv(TRAINING_DATA_PATH   + 'val_data.csv', index=False)

    def build(self):
        self.process_embedding()
        self.train_test_val_split()
        self.save_training_data()

if __name__ == '__main__':
    t = TrainingData()
    # t.build()
