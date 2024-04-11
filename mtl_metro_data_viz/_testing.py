# import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd
# np.random.seed(1)

import plotly.express as px

# from tweet import Tweet
# from interruption import Interruption
# from duration import Duration
# from sentiment import Sentiment

from _utils import BLEUE

# path = '../data/twitter_stm_rem.csv'
# tweet = Tweet(path)

# stm = Interruption(tweet.stm, '2023-01-01', '2024-12-31')
# stm_Orange = stm.get_day_with_event_heatmap('stm_Orange', 'month')


# # df = Duration(tweet.stm, 'stm_Orange').get_line_interruption_durations()
# # print(df)

# # px.histogram(df, x='date', y='duration')


# s = Sentiment().sentiment_df_light
# # s.iloc[0:100].to_csv('./test.csv', index=False)

# period = 'year'
# onehot = pd.get_dummies(s[['raw_title_sentiment', 'raw_description_sentiment']], dtype=int)
# s = pd.concat([s[period], onehot], axis=1)
# print(s.groupby(period).sum())


# print(BLEUE)

# x = pd.DataFrame.from_dict(BLEUE, orient='index', columns=['A']).loc['outremont':'fabre'].index.to_list()
# print(x)


# import plotly.express as px
# data_canada = px.data.medals_long()
# print(data_canada)


# from dash import Dash, html, dash_table, dcc, callback, Output, Input
# print(help(dcc.Slider))

print(dir(px.colors))


