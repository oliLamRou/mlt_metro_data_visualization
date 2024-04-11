# import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd
# np.random.seed(1)

# import plotly.express as px

# from tweet import Tweet
# from interruption import Interruption
# from duration import Duration
from sentiment import Sentiment

# path = '../data/twitter_stm_rem.csv'
# tweet = Tweet(path)

# stm = Interruption(tweet.stm, '2023-01-01', '2024-12-31')
# stm_Orange = stm.get_day_with_event_heatmap('stm_Orange', 'month')


# # df = Duration(tweet.stm, 'stm_Orange').get_line_interruption_durations()
# # print(df)

# # px.histogram(df, x='date', y='duration')


s = Sentiment().sentiment_df_light
# s.iloc[0:100].to_csv('./test.csv', index=False)

period = 'year'
onehot = pd.get_dummies(s[['raw_title_sentiment', 'raw_description_sentiment']], dtype=int)
s = pd.concat([s[period], onehot], axis=1)
print(s.groupby(period).sum())