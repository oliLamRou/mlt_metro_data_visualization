import os
from datetime import datetime
from ast import literal_eval

import pandas as pd
from nltk.corpus import stopwords

from mtl_metro_data_visualization.constant import _lines_stations
from mtl_metro_data_visualization.constant import _path
from mtl_metro_data_visualization.utils._utils import utc_to_local

class Tweets:
    """
    From scrapped tweets -> clean data
    1. import
    2. combine all scrap_twitter_stm_*.csv
    3. clean tweet as tweet column
    4. preprocess tweet as tweet_preprocess
    5. get date with time saving and lap year
    """
    REGEX = [
        (r"@\S*"),
        (r"#\w+"),
        (r"http\S*"),
        (r"\b\d+(\.\d+)?K\b"),
        (r"\d{1,2}h\d{2}"),
        (r"[\[\]()\/\\!?.,:;-]"),
        "bleue",
        "verte",
        "jaune",
        "orange",
        "rem",
        "a1",
    ]

    def __init__(self):
        self._df = pd.DataFrame()

    @property
    def df(self):
        if self._df.empty:
            self.ingest_scrapped_tweet()

        return self._df

    def merge_lines(self):
        for line in _lines_stations.LINES_STATIONS.keys():
            filepath = f"{_path.SCRAP_DIR}/scrap_twitter_{line}.csv"
            if not os.path.exists(filepath):
                continue

            line_df = pd.read_csv(filepath, converters={'raw_text': literal_eval})
            line_df['line'] = line
            self._df = pd.concat([self._df, line_df])

        self._df.reset_index(drop = True, inplace = True)

    def tweet_preprocessing(self):
        def remove_short_word(tweet):
            _tweet = []
            for word in tweet.split():
                if len(word) > 3:
                    _tweet.append(word)

            return " ".join(_tweet)

        #copy tweet to preprocessed
        self._df['preprocessed'] = self._df.tweet

        #lower case
        self._df.preprocessed = self._df.preprocessed.str.lower()

        #Regex match and replace with ""
        for r in self.REGEX:
            self._df.preprocessed = self._df.preprocessed.str.replace(r, "", regex=True)

        #remove short words
        self._df.preprocessed = self._df.preprocessed.apply(remove_short_word)

    def remove_english_tweets(self):
        def has_english_words(tweet):
            if set(tweet.split()) & set(swe):
                return True

            return False

        swe = []
        for word in stopwords.words('english'):
            if len(word) > 2:
                swe.append(word)

        self._df = self._df[~self._df.tweet.apply(has_english_words)]
        self._df.sort_values('raw_date', inplace=True)
        self._df.reset_index(drop=True, inplace=True)

    def ingest_scrapped_tweet(self):
        #Import and merge all line in 1 df
        self.merge_lines()

        #Join the list of string (raw_text) to make a full lengh message
        self._df['tweet'] = self._df.raw_text.apply(lambda x: " ".join(x[5:]))

        #Removing spot word and more
        self.tweet_preprocessing()

        #Removing some English tweets
        self.remove_english_tweets()

        #Converting raw_date to date(timesaving and tz)
        date = pd.to_datetime(self._df.raw_date.values, utc=True).tz_convert(tz='US/Eastern')
        self._df['date'] = date

    def tweet_contains(self, col, string):
        tweets = self.df_[self.df_[col].str.contains(string)]
        for index in tweets.index:
            print(tweets.loc[index].stop, tweets.loc[index].tweet, '\n')

if __name__ == '__main__':
    t = Tweets()
    t.ingest_scrapped_tweet()
    print(t.df.loc[582])
    # print(t.df.index.size)



