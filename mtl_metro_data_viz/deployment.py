import importlib
import pandas as pd
import numpy as np

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

import tweet
import interruption

importlib.reload(tweet)
importlib.reload(interruption)

from tweet import Tweet
from interruption import Interruption
from duration import Duration

# Incorporate data
path = '../data/twitter_stm_rem.csv'
tweet = Tweet(path)


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Interruption of service'),
    dcc.Dropdown(tweet.df.line.unique(), 'stm_Orange', id='line_dropdown'),
    dcc.Dropdown(['month', 'weekofyear', 'dayofyear'], 'month', id='period_dropdown'),
    dcc.Dropdown(['2019', '2020', '2021', '2022', '2023'], '2022', id='start_dropdown'),
    dcc.Dropdown(['2020', '2021', '2022', '2023', '2024'], '2024', id='end_dropdown'),
    dcc.Graph(figure={}, id='interruption_graph'),
    dcc.Graph(figure={}, id='duration_graph'),
    
])

@callback(
    Output(component_id =   'interruption_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_dropdown',       component_property = 'value'),
    Input(component_id =    'end_dropdown',         component_property = 'value'),
)
def update_interruption(line, period, start, end):
    if line == 'REM_infoservice':
        tweet_df = tweet.rem
    else:
        tweet_df = tweet.stm

    df = Interruption(tweet_df, f'{start}-01-01', f'{end}-12-31').get_day_with_event_heatmap(line, period)
    return px.imshow(df, x=df.columns.astype(str).values, y=df.index.astype(str).values)

@callback(
    Output(component_id =   'duration_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_dropdown',       component_property = 'value'),
    Input(component_id =    'end_dropdown',         component_property = 'value'),
)
def update_duration(line, period, start, end):
    if line == 'REM_infoservice':
        tweet_df = tweet.rem
    else:
        tweet_df = tweet.stm

    df = Duration(tweet_df, line, start, end).get_line_interruption_durations(period)
    return px.bar(df, x=period, y='duration', color='year', hover_data=df.columns, title='Duration')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)