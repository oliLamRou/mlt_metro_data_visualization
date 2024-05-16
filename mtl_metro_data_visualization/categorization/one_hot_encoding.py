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

    def get_station_range(self, stations, tweet):
        station_range = []
        tweet = tweet.lower().replace('. ', ' ').replace(',', '').split()
        
        if not 'entre' in tweet and not 'et' in tweet:
            return station_range

        for station in stations:
            #Check if name as is exist
            if station in tweet:
                station_range.append(station)

            if not '-' in station:
                continue

            #Check 2 type of abr
            abr = f'{station.split("-")[0][0]}-{station.split("-")[1]}'
            if abr in tweet:
                station_range.append(station)

            abr = f'{station.split("-")[0][0]}.-{station.split("-")[1]}'
            if abr in tweet:
                station_range.append(station)

            if 'saint' == station.split('-')[0]:
                abr = f'st-{station.split("-")[1]}'
                if abr in tweet:
                    station_range.append(station)


        #Cancel the process if more or less than 2 found
        if len(station_range) != 2:
            station_range = []

        return station_range

if __name__ == '__main__':
    oh = OneHotEncoding()
    oh.encoding()
    df = oh.df
    for tweet in df[(df.preprocessed.str.contains('entre')) & (df.stop == 1)].sample(10).preprocessed:
        print(tweet, '\n')
    # for tweet in oh.df.sample(1000)[oh.df.event == 1].preprocessed:
    #     print(tweet, '\n')