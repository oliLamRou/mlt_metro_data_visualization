import pandas as pd

def time_df(start, end):
    #Create a time serie with day as freq
    #NOTE: freq could be a parm so can check per hour
    years = pd.DataFrame(columns=['date'], data=pd.date_range(start, end, freq='d', tz='US/Eastern'))
    
    #Adding year, month, day, weekdays columns
    years['year'] = pd.to_datetime(years['date']).dt.year
    years['month'] = pd.to_datetime(years['date']).dt.month
    years['day'] = pd.to_datetime(years['date']).dt.day
    years['weekday'] = pd.to_datetime(years['date']).dt.weekday
    years['dayofyear'] = pd.to_datetime(years['date']).dt.dayofyear
    years['weekofyear'] = pd.to_datetime(years['date']).dt.isocalendar()['week']
    return years