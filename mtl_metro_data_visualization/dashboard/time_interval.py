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

    def interval_filter(self, line, columns, daily_grouping_func, interval, interval_grouping_func):
        if type(columns) != list:
            return

        #Isolate a line
        line_df = self.df[self.df.line == line]
        if line_df.empty:
            raise ValueError(f'Line name: "{line}" is not present in the DF.')

        #Get 1 day per row for the entire df. set na value to 0. max or sum values
        sum_df = line_df.resample('d', on='date')[columns].apply(daily_grouping_func)
        sum_df = self.interval_df.merge(sum_df, on='date', how='left').fillna(0)
        return sum_df.groupby(['year', interval, 'date'])[columns].apply(interval_grouping_func).reset_index()

    @staticmethod
    def date_range(df, start, end):
        return df[
            (df.date >= start) &
            (df.date <= end)
        ].reset_index(drop=True)


if __name__ == '__main__':
    t = TimeInterval()
    x = t.interval_filter('stm_orange', ['stop', 'slow', 'elevator'], max, 'month', sum)
    x = TimeInterval.date_range(x, '2022-01-01', '2023-12-31')
    print(x)
    
    # print(x)