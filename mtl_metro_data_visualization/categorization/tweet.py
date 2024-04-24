import os

from datetime import datetime, timezone
import pandas as pd
import numpy as np

from mtl_metro_data_visualization.constant._lines import BLEUE, JAUNE, ORANGE, VERTE, REM, LINES_STATIONS
from mtl_metro_data_visualization.constant.path import TWITTER_STM_REM_PATH, TWEET_ONE_HOT_PATH
from mtl_metro_data_visualization.utils._utils import utc_to_local

class Tweet:
    def __init__(self):
        self._df = pd.DataFrame()
        self.df_ = None

    @property
    def load_preprocess(self):
        self.df_ = pd.read_csv(TWEET_ONE_HOT_PATH)
        self.df_.date = pd.to_datetime(self.df_.date.values, utc=True)
        self.df_.date = self.df_.date.apply(utc_to_local)
        return self.df_

    @property
    def df(self):
        if self._df.empty:
            self._df = pd.read_csv(TWITTER_STM_REM_PATH)
            self._df.date = pd.to_datetime(self._df.date.values, utc=True)
            self._df.date = self._df.date.apply(utc_to_local)

        return self._df

    def _rem(self):
        df = self.df[self.df.line == 'REM_infoservice'].reset_index(drop=True)
        remove = 'the|with|issue|planifiée'    
        stop = 'interruption|arrêt de service'    
        slow = 'ralentissement de service|reprise'
        restart = 'rétabli|Service normal sur la ligne A1'
        return self.df_encoding(df, remove, stop, slow, restart)

    def _stm(self):
        df = self.df[self.df.line != 'REM_infoservice'].reset_index(drop=True)
        remove_english = [
            'the',
            'with',
            'issue',
            'ongoing',
            'holiday',
            'between',
            'disruption',
            'smart',
            'stopping',
            'What',
            'We'
        ]

        remove = [
            'Normal métro service',
            'Seuls les interruptions de service',
            'Planfication sensée',
            'limite temporairement la diffusion automatisée',
            'peuvent causer',
            '@.*',
            'Danny',
        ]

        stop = [
            'interruption|Arrêt ligne',
            'Arrêt prolongé ligne',
            '«utilisation du métro»',
            'reprise',
            'Perturbation du service',
            'Le service demeure au ralenti',
        ]

        restart = [
            'rétabli',
            'fin de la perturbation',
            'Service normal du métro',
            '"interruption de service .* terminée"'
        ]
        
        return self.df_encoding(
            df,
            '|'.join(remove + remove_english),
            '|'.join(stop), 
            '|'.join(restart))

    def df_encoding(self, df, remove, stop, restart):
        df_ = df.copy()
        df_ = df_[~df_.tweet.str.contains(remove, case=False)].reset_index(drop=True)
        df_['stop'] = df_.tweet.str.contains(stop, case=False).astype(int)
        df_['restart'] = df_.tweet.str.contains(restart, case=False).astype(int)

        # df_['duration'] = np.nan

        # stations = list(set(list(BLEUE.keys()) + list(JAUNE.keys()) + list(ORANGE.keys()) + list(VERTE.keys()) + list(REM.keys())))
        # stations.sort()
        
        # for station in stations:
        #     df_[station] = 0
        
        return df_

    def get_open_to_close(self, date, line=None):
        start = pd.to_datetime(f'{date} 05:00:00').tz_localize("US/Eastern")
        start, start + pd.offsets.Hour(22)
        
        return self.df_[
            (self.df_.date > start) &
            (self.df_.date < start + pd.offsets.Hour(23)) &
            (self.df_.line == line)
        ].copy()
            
    def set_duration_per_restart(self, date, line_name):
        #Get df for a single day based on open hour
        day_df = self.get_open_to_close(date, line_name)

        #Working on a single operation day
        stop_time = None
        stop_loc = None
        durations = []
        stations = set()
        
        #Loop through 1 day
        for i in day_df.index:
            row = day_df.loc[i]

            station_range = self.get_station_range(LINES_STATIONS[line_name], row.tweet)
            stations_list = self.set_interupted_stations(station_range, LINES_STATIONS[line_name])
            if stations_list:
                stations = stations.union(stations_list)
            
            #Get the first stop time if not already in an interruption
            if row.stop == 1 and stop_time == None:
                stop_time = row.date
                stop_loc = i

            #When hit a restart message, reset the clock and get the time difference
            # if row.restart == 1 and row.slow == 0 and stop_time != None:
            if row.restart == 1 and stop_time != None:
                self.df_.loc[stop_loc,'duration'] = (row.date - stop_time).seconds / 60

                #NOTE: could +1 to all stations if no specific?
                if stations:
                    self.df_.loc[stop_loc, list(stations)] = 1

                stop_time = None
                stop_loc = None

    def set_interupted_stations(self, station_range, station_dict):
        if not station_range:
            return []

        return pd.DataFrame.from_dict(
            station_dict, orient='index', columns=['order']
            ).loc[station_range[0]:station_range[1]].index.to_list()

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

    def set_duration(self, line_name):
        # years = time_df(self.start, self.end)

        duration_df = pd.DataFrame(columns=['date', 'duration'])
        for date in self.df.date.dt.strftime('%Y-%m-%d').unique():
            #Get duration per restart for a full day
            self.set_duration_per_restart(date, line_name)

    def build(self, write=False):
        # rem = self._rem()
        stm = self._stm()
        # self.df_ = pd.concat([rem, stm]).sort_values('date').reset_index(drop=True)
        self.df_ = stm.copy()

        # self.set_duration('stm_Bleue')
        # self.set_duration('stm_Jaune')
        # self.set_duration('stm_Orange')
        # self.set_duration('stm_Verte')
        # self.set_duration('REM_infoservice')
        if write:
            self._write()

    def _write(self):
        self.df_.to_csv(TWEET_ONE_HOT_PATH, index=False)

    def print_tweet(self):
        stop = self.df_[(self.df_.stop == 0) & (self.df_.restart == 0)]
        for tweet in stop.tweet.values:
            print(tweet, '\n')

    def tweet_has(self, string):
        tweets = self.df_[self.df_.tweet.str.contains(string)]
        for tweet in tweets.tweet.values:
            print(tweet, '\n')

if __name__ == '__main__':
    t = Tweet()
    t.build(write=False)

    # t.print_tweet()
    # t.tweet_has('Danny')



