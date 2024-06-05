import os
import pandas as pd
import difflib

from mtl_metro_data_visualization.categorization.tweets import Tweets
from mtl_metro_data_visualization.constant._categories import CATEGORIES
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS, ALL_STATIONS_NAME
from mtl_metro_data_visualization.constant._path import TWEET_ONE_HOT_PATH
from mtl_metro_data_visualization.utils._utils import utc_to_local

class OneHotEncoding(Tweets):
    """
    Class for performing one-hot encoding on tweets related to the Montreal metro system.
    
    Attributes:
        load_from_disk (bool): Flag to indicate if data will be load from disk.
        path (str): Path to save the one-hot encoded data.
        save (bool): Flag to indicate if the one-hot encoded data should be saved.
    """
    def __init__(self, load_from_disk=True, save=False):
        """
        Initializes the OneHotEncoding object with optional parameters.

        """        
        super().__init__()
        self.load_from_disk = load_from_disk
        self.path = TWEET_ONE_HOT_PATH

        self.save = save
        self.build()

    #STATIONS PROCESS
    def _closed_stations(self):
        #Add all stations columm set to 0
        self._df[ALL_STATIONS_NAME] = 0

        #Get stop or slow
        stop_slow_df = self.df[
            ((self.df.stop == 1) | (self.df.slow == 1)) & 
            (self.df.tweet.str.contains(r"ligne ([\w-]+) entre ([\w-]+) et ([\w-]+)", regex=True))
        ]
        #Loop rows and set 1 to station in range
        for i, row in stop_slow_df.iterrows():
            start, end = self._get_station_range(row.preprocessed)
            if not start or not end:
                continue

            line = LINES_STATIONS[row.line]
            start_index = line[start[0]]
            end_index = line[end[0]]
            stations_in_range = [station for station, index in line.items() if start_index <= index <= end_index]

            #Encoding
            self.df.loc[i, stations_in_range] = 1

    def _get_station_range(self, tweet):
        """
        Extracts the start and end stations from a tweet.

        Args:
            tweet (str): Preprocessed tweet text.

        Returns:
            tuple: Start and end station names.
        """        
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
        print('---------------------')
        for date in self.df.date.dt.strftime('%Y-%m-%d').unique():
            single_day = self._get_open_to_close(date)
            self._set_duration_per_day(single_day)

    def _get_open_to_close(self, date):
        """
        Retrieves tweets for a single day of metro operations.

        Args:
            date (str): The date for which to retrieve tweets.

        Returns:
            DataFrame: Filtered dataframe with tweets for the specified date.
        """
        start = pd.to_datetime(f'{date} 05:00:00').tz_localize("US/Eastern")
        
        return self.df[
            (self.df.date > start) &
            (self.df.date < start + pd.offsets.Hour(23))
        ]

    def _set_duration_per_day(self, single_day):
        """
        Sets the duration of interruptions per line for a single day.

        Args:
            single_day (DataFrame): DataFrame containing tweets for a single day.
        """
        stop_time = {}
        durations = []
        stations = set()
        
        for i, row in single_day.iterrows():
            line_name = row.line

            if row.stop == 1 and stop_time.get(line_name) == None:
                stop_time[line_name] = row.date

            if (row.restart == 1 or row.normal == 1 or row.slow == 1) and stop_time.get(line_name) != None:
                stop_index = single_day[single_day.date == stop_time[line_name]].index
                #Here I'm adding 10 min since stm says they only report interruption after 10 min.
                duration = ((row.date - stop_time[line_name]).seconds / 60) + 10
                self.df.loc[stop_index,'duration'] = duration

                del stop_time[line_name]

        #if stop till end of day.
        for k, v in stop_time.items():
            print('---', k, v)



    def _save(self):
        print(f'Trying saving here: {self.path}')
        self.df.to_csv(self.path, index=False)

    def build(self):
        if self.load_from_disk:
            self._df = pd.read_csv(TWEET_ONE_HOT_PATH)
            self._df.date = pd.to_datetime(self._df.date.values, utc=True)
            self._df.date = self._df.date.apply(utc_to_local)

        else:
            for k, v in CATEGORIES.items():
                self._df[k] = self.df.preprocessed.str.contains("|".join(v)).astype(int)

            self._closed_stations()
            self._set_duration()

            if self.save:
                self._save()

if __name__ == '__main__':
    oh = OneHotEncoding(load_from_disk=False, save=True)
    # for tweet in oh.df[(oh.df.line == 'rem_infoservice')][oh.df.tweet.str.contains(r"entre les stations ([\w-]+) et ([\w-]+)", regex=True)].tweet.values:
    #     print(tweet, '\n')

    # for tweet in oh.df[(oh.df.line == 'rem_infoservice')][oh.df.stop == 1].tweet.values:
    #     print(tweet, '\n')


