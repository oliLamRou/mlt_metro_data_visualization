import tensorflow as tf
assert tf.__version__ >= "2.0"

import pandas as pd

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline

class Sentiment:
    def __init__(self):
        self.sentiment_df = pd.read_csv('../data/sentiment_news_fr.csv')
        self.sentiment_df_light = pd.read_csv('../data/sentiment_news_fr_light.csv')

    def get_sentiment(df, col_name):
        #Model
        tokenizer = AutoTokenizer.from_pretrained("ac0hik/Sentiment_Analysis_French")#use_fast=True
        model = TFAutoModelForSequenceClassification.from_pretrained("ac0hik/Sentiment_Analysis_French")

        nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
        
        df_ = df.copy()

        sentiment_col = f'{col_name}_sentiment'
        score_col = f'{col_name}_sentiment_score'
        
        df[sentiment_col] = ''
        df[score_col] = 0.0
        
        for i in df.index:
            sentiment = nlp.predict(df.iloc[i][col_name])[0]
            df.loc[i,sentiment_col] = sentiment.get('label')
            df.loc[i,score_col] = sentiment.get('score')
            
        return df

    @staticmethod
    def sentiment_to_csv():
        df = pd.read_csv('../data/news_stm_rem.csv')
        df = df.fillna('')
        df = df.drop_duplicates('raw_title')
        df = df[df.source != 'gazette'].reset_index(drop=True)

        #Get for title
        title = self.get_sentiment(df, 'raw_title')
        #Get for description
        description = self.get_sentiment(title, 'raw_description')
        # Write
        description.to_csv(f'../data/sentiment_news_fr.csv', index=False)

    def sentiment_light(self):
        path = f'../data/sentiment_news_fr.csv'
        df = pd.read_csv(path)
        df.date = pd.to_datetime(df.date)

        df['year'] = ''
        df['month'] = ''
        df['weekofyear'] = ''
        df.year = df.date.dt.year
        df.month = df.date.dt.month
        df.weekofyear = df.date.dt.isocalendar()['week']
        df[['date', 'year', 'month', 'weekofyear', 'raw_title_sentiment', 'raw_description_sentiment']].to_csv('../data/sentiment_news_fr_light.csv', index=False)

if __name__ == '__main__':
    s = Sentiment().sentiment_df_light
    print(s.columns)


