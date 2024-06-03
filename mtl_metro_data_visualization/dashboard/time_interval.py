import pandas as pd
import numpy as np

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS


class TimeInterval(OneHotEncoding):
    def __init__(self, interval, load_from_disk=True, save=False):
        super().__init__(load_from_disk, save)
        self.interval = interval

        self._daily_df = pd.DataFrame()
        self._grouped_df = pd.DataFrame()
        self._filtered_df = pd.DataFrame()

        self.df_start_date = self.df.date.dt.strftime('%Y-%m-%d').min()
        self.df_end_date = self.df.date.dt.strftime('%Y-%m-%d').max() #how to get end of last month

        self.filtered_lines = list(LINES_STATIONS.keys())
        self.filtered_start = self.df.date.dt.strftime('%Y').min()
        self.filtered_end = self.df.date.dt.strftime('%Y').max()
        
        self._time_range = np.array([])

    @property
    def time_range(self):
        return self.grouped_df.interval.astype(int).sort_values().unique()

    @property
    def daily_df(self):
        if self._daily_df.empty:
            for line in self.df.line.unique():
                #Isolate line
                line_df = self.df[self.df.line == line]
                
                #Remove hour, min, sec
                line_df.loc[:,'date'] = line_df.date.dt.round('d')

                #Float -> sum, Int -> max, merge in one df on daily date.
                numeric_df = pd.merge(
                        line_df.groupby('date').sum(numeric_only=True).select_dtypes('float'),
                        line_df.groupby('date').max(numeric_only=True).select_dtypes('int'),
                        on='date', 
                        how='left'
                    )

                #Fill day gap
                df = pd.merge(
                        pd.DataFrame(
                            columns=['date'], 
                            data=pd.date_range(self.df_start_date, self.df_end_date, freq='d', tz='US/Eastern')
                        ),
                        numeric_df,
                        on='date',
                        how='left'
                    ).fillna(0)

                #Add line value
                df['line'] = line
                self._daily_df = pd.concat([self._daily_df, df])

        return self._daily_df.sort_values(['line', 'date']).reset_index(drop=True)

    @property
    def grouped_df(self):
        self._grouped_df = self.daily_df.copy()

        if self.interval == 'year':
            self._grouped_df.loc[:,'interval'] = self._grouped_df.date.dt.year
        
        elif self.interval == 'month':
            self._grouped_df.loc[:,'interval'] = self._grouped_df.date.dt.month

        elif self.interval == 'day':
            self._grouped_df.loc[:,'interval'] = self._grouped_df.date.dt.dayofyear

        elif self.interval == 'quarter':
            self._grouped_df.loc[:,'interval'] = self._grouped_df.date.dt.quarter

        else:
            raise ValueError(f"Invalid interval: {self.interval}")
    
        self._grouped_df.loc[:,'range'] = self._grouped_df.date.dt.year
        self._grouped_df = self._grouped_df.groupby(['line', 'range', 'interval']).sum(numeric_only=True).reset_index()
        # self._grouped_df.loc[:,'range'] = self._grouped_df.interval.str.split('-').str[0].astype(int)
        return self._grouped_df

    # def update_interval(self, interval):
    #     self.interval = interval
    #     return self.grouped_df

    @property
    def slice_df(self):
        return self.grouped_df[
            (self.grouped_df.range >= self.filtered_start) &
            (self.grouped_df.range <= self.filtered_end) & 
            (self.grouped_df.line.isin(self.filtered_lines))
        ].reset_index(drop=True)

    # def year_range(df, start, end):
    #     return df[
    #         (df.year >= start) &
    #         (df.year <= end)
    #     ].reset_index(drop=True)

if __name__ == '__main__':
    t = TimeInterval(
        interval = 'quarter'
    )
    # t.daily_df[['date', 'line', 'duration']].to_csv('./temp.csv', index=False)
    print(t.grouped_df[['line', 'range', 'interval']])

    #daily numerical + date
    #Fill gab with missing day and fillna(0)
    #groupby: month, weekday, etc
    #Slice

