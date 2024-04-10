from datetime import datetime, timezone
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

from tweet import Tweet
from _utils import time_df


class Interruption:
    def __init__(self, df, start, end):
        self.df = df
        self.start = start
        self.end = end

    def get_day_with_event_heatmap(self, line_name, sum_period):
        #Get full years df
        years = time_df(self.start, self.end)

        #Isolate a line
        line_df = self.df[self.df.line == line_name].reset_index(drop=True)

        #Merge on day
        sum_df = line_df.resample('d', on='date')[['stop']].max().reset_index()
        sum_df = years.merge(sum_df, on='date', how='left').fillna(0)

        #Data formatting
        sum_df = sum_df.groupby(['year', sum_period]).stop.sum().reset_index()
        sum_df = pd.pivot_table(sum_df, values='stop', columns=sum_period, index='year')
        sum_df = sum_df.sort_values('year', ascending=False)

        return sum_df

if __name__ == '__main__':
    path = '../data/twitter_stm_rem.csv'
    t = Tweet(path)

    i = Interruption(t.stm, '2022-01-01', '2024-12-31')
    x = i.get_day_with_event_heatmap('stm_Orange', 'month')
    print(np.array(x))
