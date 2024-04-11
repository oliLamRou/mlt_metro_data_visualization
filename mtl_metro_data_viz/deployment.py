import importlib
import pandas as pd
import numpy as np

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

import tweet

importlib.reload(tweet)

from tweet import Tweet
from interruption import Interruption
from duration import Duration
from sentiment import Sentiment
from station import Station
from _utils import LINES_STATIONS

intro = """
# Final Project Data Science 2024  
**Data visualization for metro line in montreal area**  
Data scrapping from mainly twitter, lapresse. The goal was to see the interruption of service in different way.
"""

interruption_title = 'Interruption of Service'
duration_title = 'Duration in minute of Interruption of Service'
station_title = 'Amount of day wiht interruption of service per station'
sentiment_title_title = 'La presse and 24h: sentiment for article title'
sentiment_title_desc = 'La presse and 24h: sentiment for article summary'

years = {
    2018: {'label': '2018'},
    2019: {'label': '2019'},
    2020: {'label': '2020'},
    2021: {'label': '2021'},
    2022: {'label': '2022'},
    2023: {'label': '2023'},
    2024: {'label': '2024'},
}

palette = px.colors.sequential.Darkmint

# Incorporate data
path = '../data/twitter_stm_rem.csv'
tweet = Tweet(path)
tweet.load_preprocess

# Initialize the app
app = Dash(__name__)

# App layout
tweet_graph = html.Div(children=[
    html.Div(children=[
        dcc.Markdown(intro),
        
        html.Br(),
        dcc.Markdown('**Metro Line**'),
        dcc.RadioItems(tweet.df_.line.unique(), 'stm_Orange', id='line_dropdown'),
        
        html.Br(),
        dcc.Markdown('**Period**'),
        dcc.RadioItems(['month', 'weekofyear', 'weekday', 'quarter'], 'month', id='period_dropdown'),
        
        html.Br(),
        dcc.Markdown('**Start Year**'),
        dcc.Slider(2018, 2024, 1, value=2019, marks = years, id = 'start_slider'),

        html.Br(),
        dcc.Markdown('**End Year**'),
        dcc.Slider(2018, 2024, 1, value=2023, marks = years, id = 'end_slider'),
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div(children=[
        dcc.Graph(figure={}, id='interruption_graph'),
        dcc.Graph(figure={}, id='duration_graph'),
        dcc.Graph(figure={}, id='station_graph'),
    ], style={'width': '70%', 'display': 'inline-block'})
], style={'display': 'flex', 'flexDirection': 'row'})

news_graph = html.Div(children=[
    html.Br(),
    dcc.Markdown("""
        # News sentiment analysis from article containning stm or rem


    """),

    dcc.Graph(figure={}, id='title_graph', style={'display': 'inline-block'}),
    dcc.Graph(figure={}, id='desc_graph', style={'display': 'inline-block'}),
])

#Layout
app.layout = html.Div([tweet_graph, news_graph])

#Interruption Chart
@callback(
    Output(component_id =   'interruption_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_slider',       component_property = 'value'),
    Input(component_id =    'end_slider',         component_property = 'value'),
)
def update_interruption(line, period, start, end):
    df = Interruption(tweet.df_, f'{start}-01-01', f'{end}-12-31').get_day_with_event_heatmap(line, period)
    return px.imshow(
        df, 
        x=df.columns.astype(str).values, 
        y=df.index.astype(str).values, 
        title=interruption_title,
        color_continuous_scale = px.colors.sequential.Plasma_r
    )

#Duration Chart
@callback(
    Output(component_id =   'duration_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_slider',       component_property = 'value'),
    Input(component_id =    'end_slider',         component_property = 'value'),
)
def update_duration(line, period, start, end):
    df = Duration(tweet.df_, line, str(start), str(end)).get_line_interruption_durations(period)
    return px.bar(
        df, 
        x=period, 
        y='duration', 
        color='year', 
        title=duration_title, 
        color_discrete_sequence = palette
    )

#Station Chart
@callback(
    Output(component_id =   'station_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_slider',       component_property = 'value'),
    Input(component_id =    'end_slider',         component_property = 'value'),
)
def update_station(line, period, start, end):
    df = Station(tweet.df_).sum_per_station(line, start, end)
    return px.histogram(df, x='station', y='stop', color='year', title=station_title, color_discrete_sequence = palette)

#Sentiment Charts
@callback(
    Output(component_id =   'title_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_slider',       component_property = 'value'),
    Input(component_id =    'end_slider',         component_property = 'value'),
)
def update_sentiment(line, period, start, end):
    df = Sentiment().sentiment_df_light
    return px.histogram(df, x='raw_title_sentiment', color='year', title=sentiment_title_title, category_orders=dict(raw_title_sentiment=['negative', 'neutral', 'positive']), color_discrete_sequence = palette)

@callback(
    Output(component_id =   'desc_graph', component_property = 'figure'),
    Input(component_id =    'line_dropdown',        component_property = 'value'),
    Input(component_id =    'period_dropdown',      component_property = 'value'),
    Input(component_id =    'start_slider',       component_property = 'value'),
    Input(component_id =    'end_slider',         component_property = 'value'),
)
def update_sentiment(line, period, start, end):
    df = Sentiment().sentiment_df_light
    return px.histogram(df, x='raw_description_sentiment', color='year', title=sentiment_title_desc, category_orders=dict(raw_description_sentiment=['negative', 'neutral', 'positive']), color_discrete_sequence = palette)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

