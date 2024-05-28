from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.time_interval import TimeInterval
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS

class DashboardSection(TimeInterval):
    def __init__(self, namespace, title, interval, load_from_disk=True, save=False):
        super().__init__(interval, load_from_disk, save)

        self.title = title
        self.graph_cumulative_id = f'{namespace}_graph_cumulative_id'
        self.graph_duration_id = f'{namespace}_graph_duration_id'
        self.slider_id = f'{namespace}_slider_id'
        self.checklist_id = f'{namespace}_checklist_id'
        self.dropdown_id = f'{namespace}_dropdown_id'
        self.stats_markdown_id = f'{namespace}_stats_markdown_id'

    @property
    def header(self):
        return html.H4(
            self.title, className="bg-primary text-white p-2 mb-2 text-center"
        )

    @property
    def interval_dropdown(self):
        return html.Div(
            [
                dbc.Label("Select Time Interval"),
                dcc.Dropdown(
                    ['year', 'quarter', 'month', 'weekday'],
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
        marks = {i: ' ' for i, interval in enumerate(self.grouped_df.interval.unique())}
        interval_split = self.grouped_df.interval.str.split('-')
        return html.Div(
            [
                dbc.Label("Select Years"),
                dcc.RangeSlider(
                    min=interval_split.str[0].astype(int).min(),
                    max=interval_split.str[0].astype(int).max(),
                    step=1,
                    value=[interval_split.str[0].astype(int).min(), interval_split.str[0].astype(int).max()],
                    id=self.slider_id,
                    tooltip={
                        "placement": "bottom", 
                        "always_visible": True,
                        "template": "{value}"
                    },
                ),
            ],
            className="mb-4",
        )

    def update_stats(self):
        return f"""
        ##### Combine Statistic
        - Average: {round(self.filtered_df[self.column].mean(), 1)}  
        - Max: {round(self.filtered_df[self.column].max(), 1)}

        """

    @property
    def stats(self):
        return html.Div([dcc.Markdown(children='placeholder', id=self.stats_markdown_id)])

    @property
    def controls(self):
        return dbc.Card(
            [self.interval_dropdown, self.line_checklist, self.interval_slider, self.stats],
            body=True,
        )

    @property
    def tabs(self):
        tab1 = dbc.Tab([dcc.Graph(id=self.graph_cumulative_id)], label="Cumulative")
        tab2 = dbc.Tab([dcc.Graph(id=self.graph_duration_id)], label="Duration")
        
        return dbc.Card(dcc.Tabs([tab1, tab2]))

    @property
    def interruption(self):
        return dbc.Row([
                self.header,
                dbc.Col([
                    self.controls,
                ]),
                dbc.Col([self.tabs], width=8),
            ])

    # @property
    # def IO(self):
    #     out_ = [
    #             Output(self.graph_id, 'figure'),
    #             Output(self.stats_markdown_id, 'children'),
    #         ]
    #     in_ = [
    #             Input(self.slider_id, 'value'),
    #             Input(self.checklist_id, 'value'),
    #             Input(self.dropdown_id, 'value')
    #         ]
    #     return out_, in_

    @property
    def multi_line_interruption(self):
        return dbc.Row([
                self.header,
                dbc.Col([
                    dbc.Card(
                        [self.line_checklist, self.interval_slider, self.stats],
                        body=True,
                    )
                ]),
                dbc.Col([self.tabs], width=8),
            ])

    @property
    def multi_line_interruption_IO(self):
        out_ = [
                Output(self.graph_cumulative_id, 'figure'),
                Output(self.graph_duration_id, 'figure'),
                Output(self.stats_markdown_id, 'children'),
            ]
        in_ = [
                Input(self.slider_id, 'value'),
                Input(self.checklist_id, 'value')
            ]
        return out_, in_
