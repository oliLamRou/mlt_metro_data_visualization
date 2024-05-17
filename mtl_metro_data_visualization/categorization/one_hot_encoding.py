import os
import pandas as pd
import difflib

from mtl_metro_data_visualization.categorization.tweets import Tweets
from mtl_metro_data_visualization.constant._categories import CATEGORIES
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS, ALL_STATIONS_NAME
from mtl_metro_data_visualization.constant._path import TWEET_ONE_HOT_PATH
from mtl_metro_data_visualization.utils._utils import utc_to_local

class OneHotEncoding(Tweets):
    def __init__(self, on_disk=False, path=None, save=False):
        super().__init__()
        self.on_disk = on_disk
        if path:
            self.path = path
        else:
            self.path = TWEET_ONE_HOT_PATH

        self.save = save

    #STATIONS PROCESS
    def _closed_stations(self):
        #Add all stations columm set to 0
        oh._df[ALL_STATIONS_NAME] = 0

        #Get stop or slow
        stop_slow_df = self.df[
            ((self.df.stop == 1) | (self.df.slow == 1)) & 
            (self.df.tweet.str.contains(r"ligne ([\w-]+) entre ([\w-]+) et ([\w-]+)", regex=True))
        ]
        #Loop rows and set 1 to station in range
        for i, row in stop_slow_df.iterrows():
            start, end = oh._get_station_range(row.preprocessed)
            if not start or not end:
                continue

            line = LINES_STATIONS[row.line]
            start_index = line[start[0]]
            end_index = line[end[0]]
            stations_in_range = [station for station, index in line.items() if start_index <= index <= end_index]

            #Encoding
            self._df.loc[i, stations_in_range] = 1

    def _get_station_range(self, tweet):
        # tweet = tweet.replace('.', '').replace(',', '').lower()
        words = tweet.split()
        start = []
        end = []
        for i in range(len(words)):
            if words[i] == 'ligne' and words[i + 1] == 'entre' and i+4 < len(words):
                start = difflib.get_close_matches(words[i + 2], ALL_STATIONS_NAME, n=1)
                end = difflib.get_close_matches(words[i + 3], ALL_STATIONS_NAME, n=1)

        return start, end

    #DURATION PROCESS
    def _set_duration(self):
        for date in self.df.date.dt.strftime('%Y-%m-%d').unique():
            single_day = self._get_open_to_close(date)
            self._set_duration_per_day(single_day)

    def _get_open_to_close(self, date):
        start = pd.to_datetime(f'{date} 05:00:00').tz_localize("US/Eastern")
        start, start + pd.offsets.Hour(22)
        
        return self.df[
            (self.df.date > start) &
            (self.df.date < start + pd.offsets.Hour(23))
        ]

    def _set_duration_per_day(self, single_day):
        #Working on a single operation day
        stop_time = {}
        durations = []
        stations = set()
        
        #Loop through 1 day
        for i, row in single_day.iterrows():
            line_name = row.line

            #Get the first stop time if not already in an interruption
            if row.stop == 1 and stop_time.get(line_name) == None:
                stop_time[line_name] = row.date

            #When hit a restart message, reset the clock and get the time difference
            if (row.restart == 1 or row.normal == 1) and stop_time.get(line_name) != None:
                stop_index = single_day[single_day.date == stop_time[line_name]].index
                #Here I'm adding 10 min since stm says they only report interruption after 10 min.
                duration = ((row.date - stop_time[line_name]).seconds / 60) + 10
                self.df.loc[stop_index,'duration'] = duration

                del stop_time[line_name]

    def _save(self):
        if self.path:
            print(f'Saving here: {TWEET_ONE_HOT_PATH}')
            self.df.to_csv(self.path, index=False)
        else:
            print("Saving failed because there no path specified.")

    def build(self):
        if self.on_disk:
            self._df = pd.read_csv(TWEET_ONE_HOT_PATH)
            self._df.date = pd.to_datetime(self._df.date.values, utc=True)
            self._df.date = self._df.date.apply(utc_to_local)

        else:
            for k, v in CATEGORIES.items():
                self._df[k] = self.df.preprocessed.str.contains("|".join(v)).astype(int)

            self._closed_stations()
            self._set_duration()

        if not self.on_disk and self.save:
            self._save()

if __name__ == '__main__':
    oh = OneHotEncoding(on_disk=True)
    oh.build()
    print(oh.df.info())



