from datetime import datetime, timezone
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

from tweet import Tweet
from _utils import time_df

class Duration:
    def __init__(self, df, line_name, start, end):
        self.df = df
        self.line_name = line_name
        self.start = start
        self.end = end

    def get_open_to_close(self, date, line=None):
        start = pd.to_datetime(f'{date} 05:00:00').tz_localize("US/Eastern")
        start, start + pd.offsets.Hour(22)
        
        return self.df[
            (self.df.date > start) &
            (self.df.date < start + pd.offsets.Hour(23)) &
            (self.df.line == line)
        ].copy()
            
    def get_single_day_interruption_durations(self, date):
        #Get df for a single day based on open hour
        line_df = self.get_open_to_close(date, self.line_name)

        #Working on a single operation day
        stop_time = None
        durations = []
        
        #Loop through 1 day
        for i in line_df.index:
            row = line_df.loc[i]
            
            #Get the first stop time if not already in an interruption
            if row.stop == 1 and stop_time == None:
                stop_time = row.date

            #When hit a restart message, reset the clock and get the time difference
            if row.restart == 1 and row.slow == 0 and stop_time != None:
                durations.append([row.date, (row.date - stop_time).seconds / 60])
                stop_time = None
                
        return durations

    def get_line_interruption_durations(self, period):
        years = time_df(self.start, self.end)

        duration_df = pd.DataFrame(columns=['date', 'duration'])
        for date in self.df.date.dt.strftime('%Y-%m-%d').unique():
            #Get duration per even for a full day
            single_day_durations = self.get_single_day_interruption_durations(date)
            
            #NOTE: This could probably be replace by getting a df from 'get_single_day_interruption_durations'
            if single_day_durations:
                for duration in single_day_durations:
                    duration_df.loc[len(duration_df.index)] = duration

        duration_df.duration = duration_df.duration.astype(int)
        sum_df = duration_df.resample('d', on='date')[['duration']].max().reset_index()
        sum_df = years.merge(sum_df, on='date', how='left').fillna(0)
        sum_df = sum_df.groupby(['year', period])['duration'].sum().reset_index()
        return sum_df

if __name__ == '__main__':
    path = '../data/twitter_stm_rem.csv'
    tweet = Tweet(path)
    duration = Duration(tweet.stm, 'stm_Orange', '2022-01-01', '2024-12-31')
    df = duration.get_line_interruption_durations('month')
    print(df.info())





