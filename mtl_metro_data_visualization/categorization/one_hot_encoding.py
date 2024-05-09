import pandas as pd

from mtl_metro_data_visualization.categorization.tweets import Tweets
from mtl_metro_data_visualization.constant._categories import CATEGORIES

class OneHotEncoding(Tweets):
    def __init__(self):
        super().__init__()

    def encoding(self):
        for k, v in CATEGORIES.items():
            self._df[k] = self.df.preprocessed.str.contains("|".join(v)).astype(int)

    def interruption_duration(self):
        #from first interruption to back to normal
        pass

    def closed_stations(self):
        #get 1 in station if closed, interruption or slow service.
        #need to between x station and y station function
        pass

if __name__ == '__main__':
    oh = OneHotEncoding()
    oh.encoding()
    oh._df = oh.df.sort_values('preprocessed')
    for tweet in oh.df[oh.df.stop == 1].preprocessed:
        print(tweet)