import pandas as pd
import numpy as np 

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf

from mtl_metro_data_visualization.categorization.tweet import Tweet
from mtl_metro_data_visualization.constant.path import TRAINING_DATA_PATH

class TrainingData:
    EMBEDDING_MODEL_PATH = '../../model/sentence-camenbert-base'

    def __init__(self):
        self._df = pd.DataFrame()

        self._embedding_model = None
        self._vectorizer = None
        self._tfidf = None
        self._training_data = pd.DataFrame()

        self.train_data = pd.DataFrame()
        self.test_data = pd.DataFrame()
        self.val_data = pd.DataFrame()

    @property
    def df(self):
        if self._df.empty:
            self._df = Tweet().load_preprocess.copy()

        return self._df

    @property
    def training_data(self):
        if self._training_data.empty:
            self._training_data = self.df[['tweet', 'stop']].copy()

        return self._training_data

    @property
    def embedding_model(self):
        if self._embedding_model == None:
            #NOTE: not sure if should load model everytime
            # model =  SentenceTransformer("Sahajtomar/french_semantic")
            # model.save(EMBEDDING_MODEL_PATH)
            self._embedding_model = SentenceTransformer(self.EMBEDDING_MODEL_PATH)

        return self._embedding_model

    def string_cleaning(self):
        #NOTE: URL, g 1 23 3.3k, missing
        pattern = '|'.join(
            [
                '#stminfo',
                '#stm',
                '!',
                'http\S+',
                '\s+[a-z]\s+.*\s+.*k$',
                '\s+[0-9]^\s\d{3}'
            ])

        self.training_data.tweet = self.training_data.tweet.str.lower().replace(pattern, '', regex=True)

    def sentence_to_vec(self, sentence):
        return list(self.embedding_model.encode(sentence))

    def train_test_val_split(self):
        self.train_data, temp = train_test_split(self.training_data, test_size=0.25)
        self.test_data, self.val_data = train_test_split(temp, test_size=0.5)
        
    def add_tfidf(self):
        self._vectorizer = TfidfVectorizer()
        self._tfidf = self._vectorizer.fit_transform(self.training_data.tweet)
        self.training_data['embedding'] = list(self._tfidf.toarray())

    def process_embedding(self):
        #For now working only on tweet + stop
        self.training_data['embedding'] = self.df['tweet'].apply(self.sentence_to_vec)

        return self.training_data

    def save_training_data(self):
        self.train_data.to_csv(TRAINING_DATA_PATH + 'train_data.csv', index=False)
        self.test_data.to_csv(TRAINING_DATA_PATH  + 'test_data.csv', index=False)
        self.val_data.to_csv(TRAINING_DATA_PATH   + 'val_data.csv', index=False)

    def build(self):
        self.string_cleaning()
        # self.process_embedding()
        self.add_tfidf()

        # tf.keras.layers.TextVectorization(
        #     max_tokens=None,
        #     standardize='lower_and_strip_punctuation',
        #     split='whitespace',
        #     ngrams=None,
        #     output_mode='int',
        #     output_sequence_length=None,
        #     pad_to_max_tokens=False,
        #     vocabulary=None,
        #     idf_weights=None,
        #     sparse=False,
        #     ragged=False,
        #     encoding='utf-8',
        #     name=None
        # )
        
        self.train_test_val_split()
        self.save_training_data()

if __name__ == '__main__':
    t = TrainingData()
    t.build()
    print(t.train_data['embedding'][0].shape)
    # pattern = '|'.join(['#stminfo', '#stm', '!', 'http\S+', '\s+[a-z]\s+.*\s+.*k$', '\s+[0-9]^\s\d{3}'])
    # df = t.df.tweet.str.lower().replace(pattern, '', regex=True)
    # for s in df.values:
    #     print(s, '\n')

