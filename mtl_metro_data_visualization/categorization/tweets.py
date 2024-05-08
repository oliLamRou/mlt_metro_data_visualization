import os
from datetime import datetime, timezone
from ast import literal_eval

import pandas as pd

from mtl_metro_data_visualization.constant import _lines
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
        "BLEUE",
        "VERTE",
        "JAUNE",
        "ORANGE",
        "REM",
        "A1",
    ]

    def __init__(self):
        self._df = pd.DataFrame()

    @property
    def df(self):
        if self._df.empty:
            self.ingest_scrapped_tweet()

        return self._df

    def merge_lines(self):
        for line in _lines.LINES_STATIONS.keys():
            filepath = f"{_path.SCRAP_DIR}/raw_twitter_{line}.csv"
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

        #Regex match and replace with ""
        for r in self.REGEX:
            self._df.preprocessed = self._df.preprocessed.str.replace(r, "", regex=True)

        #remove short words
        self._df.preprocessed = self._df.preprocessed.apply(remove_short_word)

    def ingest_scrapped_tweet(self):
        #Import and merge all line in 1 df
        self.merge_lines()

        #Take raw_text col and make a simple tweet col with only main message
        self._df['tweet'] = self._df.raw_text.apply(lambda x: " ".join(x[5:]))
        self.tweet_preprocessing()

    def tweet_contains(self, col, string):
        tweets = self.df_[self.df_[col].str.contains(string)]
        for index in tweets.index:
            print(tweets.loc[index].stop, tweets.loc[index].tweet, '\n')

if __name__ == '__main__':
    t = Tweets()
    t.ingest_scrapped_tweet()
    print(t.df)



