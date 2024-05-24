import pandas as pd
import numpy as np

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS


class TimeInterval(OneHotEncoding):
    def __init__(self, column, daily_grouping_func, interval_grouping_func, interval, load_from_disk=True, save=False):
        super().__init__(load_from_disk, save)
        self.column = column
        self.daily_grouping_func = daily_grouping_func
        self.interval_grouping_func = interval_grouping_func 
        self.interval = interval

        self._interval_df = pd.DataFrame()
        self._grouped_df = pd.DataFrame()
        self._filtered_df = pd.DataFrame()

        self.df_start_date = self.df.date.dt.strftime('%Y-%m-%d').min()
        self.df_end_date = self.df.date.dt.strftime('%Y-%m-%d').max()

        self.filtered_lines = list(LINES_STATIONS.keys())
        self.filtered_start = self.df.date.dt.strftime('%Y').min()
        self.filtered_end = self.df.date.dt.strftime('%Y').max()
        
        self._time_range = np.array([])

    @property
    def interval_df(self):
        if self._interval_df.empty:
            self._interval_df = pd.DataFrame(columns=['date'], data=pd.date_range(
                self.df_start_date, self.df_end_date, freq='d', tz='US/Eastern'))
            
            self._interval_df['year'] = pd.to_datetime(self._interval_df['date']).dt.year
            self._interval_df['month'] = pd.to_datetime(self._interval_df['date']).dt.month
            self._interval_df['day'] = pd.to_datetime(self._interval_df['date']).dt.day
            self._interval_df['weekday'] = pd.to_datetime(self._interval_df['date']).dt.weekday
            self._interval_df['quarter'] = pd.to_datetime(self._interval_df['date']).dt.quarter
            self._interval_df['weekofyear'] = pd.to_datetime(self._interval_df['date']).dt.isocalendar()['week']

            self._interval_df['dayofyear'] = pd.to_datetime(self._interval_df['date']).dt.dayofyear
        
        return self._interval_df

    def _filter(self, line):
        #Filter Line
        df = self.df[self.df.line == line]

        #Group on daily
        df = df.resample('d', on='date')
        
        #Combine funtion, sum, avg, max, min etc
        df = df[self.column].apply(self.daily_grouping_func)

        #Merge with full daily df to have every day of the year between start and end of the DF
        df = self.interval_df.merge(df, on='date', how='left').fillna(0)

        #Return daily if no interval
        if not self.interval:
            df.date = df.date.dt.strftime('%Y-%m-%d').reset_index(drop=True)
            return df[['date'] + self.column]
        

        groupby_column_list = ['year', 'date']
        #MONTH     
        if self.interval == 'month':
            df.date = df.date.dt.strftime('%Y-%m').reset_index(drop=True)

        #
        elif self.interval in ['dayofyear', 'year']:
            df.date = df[self.interval]
            if self.interval == 'dayofyear':
                groupby_column_list.append('dayofyear')

        else:
            df.date = df.year.astype(str) + '-' + df[self.interval].astype(str)

        return df.groupby(groupby_column_list)[self.column].apply(self.interval_grouping_func).reset_index()

    def update_interval(self, interval):
        self.interval = interval
        self.process_grouped_df()
        return self._grouped_df

    def process_grouped_df(self):
        self._grouped_df = pd.DataFrame()
        for line in self.df.line.unique():
            df = self._filter(line)
            df['line'] = line
            self._grouped_df = pd.concat([self._grouped_df, df])

    @property
    def grouped_df(self):
        if self._grouped_df.empty:
            self.process_grouped_df()

        return self._grouped_df

    @property
    def filtered_df(self):
        #Filter Lines with list of name
        self._filtered_df = self.grouped_df[
            self.grouped_df.line.isin(self.filtered_lines)
        ]
        
        #Filter by start and end year
        self._filtered_df = self.year_range(self._filtered_df, self.filtered_start, self.filtered_end)
        return self._filtered_df

    @property
    def time_range(self):
        if not self._time_range.size:
            df = self.grouped_df
            if self.interval == 'dayofyear':
                self._time_range = df.dayofyear.astype(int).sort_values().unique()
            else:    
                self._time_range = df.year.astype(int).sort_values().unique()
        
        return self._time_range

    def year_range(df, start, end):
        return df[
            (df.year >= start) &
            (df.year <= end)
        ].reset_index(drop=True)

if __name__ == '__main__':
    t = TimeInterval(
        column = 'stop',
        daily_grouping_func = max,
        interval_grouping_func = sum,
        interval = 'month'
    )
    df = t.df.copy()
    #Remove hour, min, sec
    df.date = df.date.dt.round('d')
    #Groupby line and date
    grouped_df = df.groupby(['line', 'date'])
    #Merge with sum all float
    df = t.interval_df.merge(
            grouped_df.sum().select_dtypes('float').reset_index(), 
            on='date', 
            how='left'
        ).fillna(0)

    #Merge with max all int
    df = df.merge(
            df.max(numeric_only=True).select_dtypes('int'),
            on='date', 
            how='left'
        ).fillna(0)
    


