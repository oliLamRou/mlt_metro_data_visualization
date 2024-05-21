import pandas as pd

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding


class TimeInterval(OneHotEncoding):
    def __init__(self, load_from_disk=True, save=False):
        super().__init__(load_from_disk, save)
        self._interval_df = pd.DataFrame()

    @property
    def interval_df(self):
        if self._interval_df.empty:
            #get start and end from self.df
            start = self.df.date.dt.strftime('%Y-%m-%d').min()
            end = self.df.date.dt.strftime('%Y-%m-%d').max()
            
            self._interval_df = pd.DataFrame(columns=['date'], data=pd.date_range(start, end, freq='d', tz='US/Eastern'))
            
            self._interval_df['year'] = pd.to_datetime(self._interval_df['date']).dt.year
            self._interval_df['month'] = pd.to_datetime(self._interval_df['date']).dt.month
            self._interval_df['day'] = pd.to_datetime(self._interval_df['date']).dt.day
            self._interval_df['weekday'] = pd.to_datetime(self._interval_df['date']).dt.weekday
            self._interval_df['dayofyear'] = pd.to_datetime(self._interval_df['date']).dt.dayofyear
            self._interval_df['quarter'] = pd.to_datetime(self._interval_df['date']).dt.quarter
            self._interval_df['weekofyear'] = pd.to_datetime(self._interval_df['date']).dt.isocalendar()['week']
        
        return self._interval_df

    def get_line_daily(self, line):
        line_df = self.df[self.df.line == line]
        if line_df.empty:
            raise ValueError(f'Line name: "{line}" is not present in the DF.')

        return line_df.resample('d', on='date')        

    def filter(self, line=None, column_list=None, daily_grouping_func=None, interval_grouping_func=None, interval=None):
        #Line
        df = self.df[self.df.line == line]
        if df.empty:
            raise ValueError(f'Line name: "{line}" is not present in the DF.')

        #Group on daily
        df = df.resample('d', on='date')
        
        #Combine funtion, sum, avg, max, min etc
        df = df[column_list].apply(daily_grouping_func)

        #Merge with full daily df to have every day of the year between start and end of the DF
        df = self.interval_df.merge(df, on='date', how='left').fillna(0)

        #Group by interval longer than daily
        if not interval:
            return df.reset_index()
        
        group_column_list = [interval]
        if interval != 'year':
            group_column_list = ['year'] + group_column_list

        return df.groupby(group_column_list)[column_list].apply(interval_grouping_func).reset_index()
        
    @staticmethod
    def year_range(df, start, end):
        return df[
            (df.year >= start) &
            (df.year <= end)
        ].reset_index(drop=True)


if __name__ == '__main__':
    t = TimeInterval()
    df = t.filter(
        line = 'stm_orange',
        column_list = ['stop', 'slow'],
        interval = 'weekofyear',
        daily_grouping_func = max,
        interval_grouping_func = sum
    )

    df = TimeInterval.year_range(df, 2016, 2023)
    print(df)