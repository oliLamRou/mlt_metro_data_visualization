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
            self._interval_df['quarter'] = pd.to_datetime(self._interval_df['date']).dt.quarter
            self._interval_df['weekofyear'] = pd.to_datetime(self._interval_df['date']).dt.isocalendar()['week']

            self._interval_df['dayofyear'] = pd.to_datetime(self._interval_df['date']).dt.dayofyear
        
        return self._interval_df

    def _filter(self, line, column_list, daily_grouping_func, interval_grouping_func=None, interval=None):
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


        if not interval:
            df.date = df.date.dt.strftime('%Y-%m-%d').reset_index(drop=True)
            return df[['date'] + column_list]

        #Group by interval longer than daily
        groupby_column_list = ['year', 'date']
        if interval == 'month':
            df.date = df.date.dt.strftime('%Y-%m').reset_index(drop=True)
        elif interval in ['dayofyear', 'year']:
            df.date = df[interval]
            #remove year from list
            if interval == 'year':
                groupby_column_list = ['date']
        else:
            #Else need to combine to keep year + interval
            df.date = df.year.astype(str) + '-' + df[interval].astype(str)

        return df.groupby(groupby_column_list)[column_list].apply(interval_grouping_func).reset_index()
        
    def time_grouping(self, column_list=None, daily_grouping_func=None, interval_grouping_func=None, interval=None):
        all_line = pd.DataFrame()
        for line in self.df.line.unique():
            df = self._filter(
                line = line,
                column_list = column_list,
                interval = interval,
                daily_grouping_func = daily_grouping_func,
                interval_grouping_func = interval_grouping_func
            )
            df['line'] = line
            all_line = pd.concat([all_line, df])

        return all_line


    @staticmethod
    def year_range(df, start, end):
        return df[
            (df.year >= start) &
            (df.year <= end)
        ].reset_index(drop=True)


if __name__ == '__main__':
    t = TimeInterval()
    all_line = t._filter(
                line = 'stm_orange',
                column_list = ['stop', 'slow'],
                daily_grouping_func = max,
                interval_grouping_func = sum,
                interval = 'weekday'
            )

    all_line = TimeInterval.year_range(all_line, 2022, 2023)
    print(all_line)


