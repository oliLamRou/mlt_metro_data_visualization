from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
from mtl_metro_data_visualization.utils._utils import get_time_interval_df
# from app.style import SIDEBAR_STYLE, CONTENT_STYLE
# from app.form import Form

#Data interval
#Year, Quarter, Month, Week, All

#Data
"""
- Amount of Interruption
- Duration of Interruption
- Elevator Down
- Per Station Interruption
"""

oh = OneHotEncoding(load_from_disk=True)
fig = px.scatter(oh.df, x="date", y="duration", color='line')
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

def 

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
            dcc.Markdown("SOMEHTING"),
            dcc.Graph(figure=fig)
            # dbc.Container(form.form, style=SIDEBAR_STYLE, id='form_container-id'),
            # dbc.Container(form.cards, style=CONTENT_STYLE, id='cards_container-id')
        ]
    )
    app.run(debug=True)