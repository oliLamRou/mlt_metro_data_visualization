import importlib
from datetime import datetime, timezone
import pandas as pd

import tweet
importlib.reload(tweet)

from tweet import Tweet
from _utils import utc_to_local, time_df, LINES_STATIONS

class Station:
    def __init__(self, df):
        self.df = df
        self.df_ = None

    def sum_per_station(self, line_name, start, end):
        df = self.df.copy()
        #load
        df = pd.read_csv('../data/tweet.csv')
        df.date = pd.to_datetime(df.date.values, utc=True)
        df.date = df.date.apply(utc_to_local)

        #get single line
        df = df[df.line == line_name]

        #keep only line col and group by day
        df = df.resample('d', on='date')[list(LINES_STATIONS[line_name].keys())].max().fillna(0).reset_index()

        #create year month ...
        df['year'] = 0
        df.year = df.date.dt.year

        df = df[(df.year >= int(start)) & (df.year <= int(end))]

        #group by
        df = df.groupby(['year'])[list(LINES_STATIONS[line_name].keys())].sum().reset_index()

        new = pd.DataFrame(columns=['station', 'year', 'stop'])
        for col in df.columns:
            new_station = pd.DataFrame(columns=['station', 'year', 'stop'])
            if col in ['year']:
                continue

            new_station[['year', 'stop']] = df[['year', col]]
            new_station['station'] = col
            new = pd.concat([new, new_station])

        return new

if __name__ == '__main__':
    #load
    path = '../data/twitter_stm_rem.csv'
    t = Tweet(path)
    t.build()
    # t.load_preprocess
    df = t.df_
    rem = df[df.line == 'REM_infoservice']
    s = Station(t.df_).sum_per_station('REM_infoservice', '2023', '2024')
    print(s)


    rem_stations = list(LINES_STATIONS['REM_infoservice'].keys())
    print(rem[rem_stations].sum())



