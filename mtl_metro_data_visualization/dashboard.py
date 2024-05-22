from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
# from mtl_metro_data_visualization.utils._utils import get_time_interval_df
from mtl_metro_data_visualization.dashboard.time_interval import TimeInterval
# from app.style import SIDEBAR_STYLE, CONTENT_STYLE
# from app.form import Form

#Data interval
#Year, Quarter, Month, Week, All

#Data
"""
- Amount of Day with at least 1 Interruption of service, line chart with all lines with proper color
- Duration of Interruption
- Elevator Down
- Per Station Interruption
"""

t = TimeInterval()
df = t.time_grouping(
    column_list = ['stop'],
    daily_grouping_func = max,
    interval_grouping_func = sum,
    interval = 'month'
)

fig = px.bar(df, x='date', y='stop', color='line')
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
message = """
Average: 
Amount:
bla bla:
"""


@app.callback(
    Output('interruption_graph_id', 'figure'),
    [
        Input('year_range_slider_id', 'value'),
    ]
)
def year_range_slider(year_range):
    df_ = TimeInterval.year_range(df, year_range[0], year_range[1])
    return px.bar(df_, x='date', y='stop', color='line')

if __name__ == '__main__':
    # form = Form()
    app.layout = html.Div(
        [
            dcc.Markdown("Amount of day with at least 1 interruption of service."),
            dcc.Graph(figure=fig, id='interruption_graph_id'),
            dcc.RangeSlider(value=[2019, 2020], step=1, marks={i: str(i) for i in range(2018, 2024, 1)}, id='year_range_slider_id'),
        ]
    )
    app.run(debug=True)