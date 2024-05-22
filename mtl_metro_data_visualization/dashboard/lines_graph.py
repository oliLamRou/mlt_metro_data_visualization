from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.time_interval import TimeInterval
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS

class LinesGraph(TimeInterval):
    def __init__(self, namespace, columns, daily_grouping_func, interval_grouping_func, interval, load_from_disk=True, save=False):
        super().__init__(columns, daily_grouping_func, interval_grouping_func, interval, load_from_disk, save)

        self.graph_id = f'{namespace}_graph_id'
        self.slider_id = f'{namespace}_slider_id'
        self.checklist_id = f'{namespace}_checklist_id'
        self.dropdown_id = f'{namespace}_dropdown_id'

    @property
    def header(self):
        return html.H4(
            "Interruptions", className="bg-primary text-white p-2 mb-2 text-center"
        )

    @property
    def interval_dropdown(self):
        return html.Div(
            [
                dbc.Label("Select Time Interval"),
                dcc.Dropdown(
                    ['year', 'month', 'day', 'weekday', 'quarter'],
                    "year",
                    id=self.dropdown_id,
                    clearable=False,
                ),
            ],
            className="mb-4",
        )

    @property
    def line_checklist(self):
        return html.Div(
            [
                dbc.Label("Select Metro Line"),
                dbc.Checklist(
                    id=self.checklist_id,
                    options=list(LINES_STATIONS.keys()),
                    value=list(LINES_STATIONS.keys()),
                    inline=True,
                ),
            ],
            className="mb-4",
        )

    @property
    def interval_slider(self):
        return html.Div(
            [
                dbc.Label("Select Years"),
                dcc.RangeSlider(
                    min(self.time_range), 
                    max(self.time_range),
                    1,
                    id=self.slider_id,
                    marks=None,
                    value=[min(self.time_range), max(self.time_range)],
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="p-0",
                ),
            ],
            className="mb-4",
        )

    @property
    def controls(self):
        return dbc.Card(
            [self.interval_dropdown, self.line_checklist, self.interval_slider],
            body=True,
        )

    @property
    def tabs(self):
        return dbc.Card(
            dcc.Graph(id=self.graph_id)
        )

    @property
    def interruption(self):
        return dbc.Row([
                self.header,
                dbc.Col([
                    self.controls,
                ]),
                dbc.Col([self.tabs], width=8),
            ])

    @property
    def IO(self):
        out_ = Output(self.graph_id, 'figure')
        in_ = [
                Input(self.slider_id, 'value'),
                Input(self.checklist_id, 'value'),
                Input(self.dropdown_id, 'value')
            ]
        return out_, in_
