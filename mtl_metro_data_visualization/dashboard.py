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

# oh = OneHotEncoding(load_from_disk=True)
t = TimeInterval()
df = t.filter(
    line = 'stm_orange',
    column_list = ['stop', 'slow'],
    interval = 'year',
    daily_grouping_func = max,
    interval_grouping_func = sum
)
fig = px.scatter(df, x="year", y="stop")
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
message = """
Average: 
Amount:
bla bla:
"""


#SAVE CLEAR
# @app.callback(
#     [
#         Output('cards_container-id', 'children'),
#     ],
#     [
#         Input('save-button-id', 'n_clicks'),
#     ],
#     [
#         State('title-id', 'value'),
#     ])
# def save_clear_button(save, clear, title, note, selected_category, new_category, value):
#     category_value = new_category if selected_category == 'new category' else selected_category

#     if ctx.triggered_id == 'save-button-id':
#         form.new_entry('title', title)
#         form.new_entry('note', note)
#         form.new_entry(category_value, value)
#         form.save()

#     return form.cards, form.form

if __name__ == '__main__':
    # form = Form()
    app.layout = html.Div(
        [
            dcc.Markdown("Amount of day with at least 1 interruption of service."),
            dcc.Graph(figure=fig),
            dcc.Markdown('_'),
            dcc.RangeSlider(2019, 2020, 1, marks={2019: '2019', 2020: '2020'}, id='year_range_slider'),
            dcc.Markdown(message)
            # dbc.Container(form.form, style=SIDEBAR_STYLE, id='form_container-id'),
            # dbc.Container(form.cards, style=CONTENT_STYLE, id='cards_container-id')
        ]
    )
    app.run(debug=True)