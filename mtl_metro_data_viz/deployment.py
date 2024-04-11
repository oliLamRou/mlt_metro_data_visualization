import importlib
import pandas as pd
import numpy as np

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

from tweet import Tweet
from interruption import Interruption
from duration import Duration
from sentiment import Sentiment

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
    dcc.Graph(figure={}, id='title_graph', style={'display': 'inline-block'}),
    dcc.Graph(figure={}, id='desc_graph', style={'display': 'inline-block'}),
    
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

@callback(
    Output(component_id =   'title_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_dropdown',       component_property = 'value'),
    Input(component_id =    'end_dropdown',         component_property = 'value'),
)
def update_sentiment(line, period, start, end):
    df = Sentiment().sentiment_df_light
    return px.histogram(df, x='raw_title_sentiment', color='year', title='Sentiment From Article Title', category_orders=dict(raw_title_sentiment=['negative', 'neutral', 'positive']))

@callback(
    Output(component_id =   'desc_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_dropdown',       component_property = 'value'),
    Input(component_id =    'end_dropdown',         component_property = 'value'),
)
def update_sentiment(line, period, start, end):
    df = Sentiment().sentiment_df_light
    return px.histogram(df, x='raw_description_sentiment', color='year', title='Sentiment From Article Summary', category_orders=dict(raw_description_sentiment=['negative', 'neutral', 'positive']))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

