from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.time_interval import TimeInterval
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS
from mtl_metro_data_visualization.dashboard import markdown

class DashboardSection(TimeInterval):
    def __init__(self, namespace, title, interval, load_from_disk=True, save=False):
        super().__init__(interval, load_from_disk, save)

        self.title = title

        #Name Spaces
        self.graph_cumulative_id = f'{namespace}_graph_cumulative_id'
        self.graph_duration_id = f'{namespace}_graph_duration_id'
        self.slider_id = f'{namespace}_slider_id'
        self.checklist_id = f'{namespace}_checklist_id'
        self.radioItems_id = f'{namespace}_radioItems_id'
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
    def line_radioItems(self):
        return html.Div(
            [
                dbc.Label("Select Metro Line"),
                dbc.RadioItems(
                    id=self.radioItems_id,
                    options=list(LINES_STATIONS.keys()),
                    value='stm_verte',
                    inline=True,
                ),
            ],
            className="mb-4",
        )

    @property
    def interval_slider(self):
        marks = {interval: str(interval) for interval in range(self.grouped_df.range.min(), self.grouped_df.range.max())}
        return html.Div(
            [
                dbc.Label("Select Years"),
                dcc.RangeSlider(
                    min=self.grouped_df.range.min(),
                    max=self.grouped_df.range.max(),
                    step=1,
                    value=[self.grouped_df.range.min(), self.grouped_df.range.max(),],
                    id=self.slider_id,
                    marks=marks,
                    tooltip={
                        "placement": "bottom", 
                        "always_visible": True,
                        "template": "{value}"
                    },
                ),
            ],
            className="mb-4",
        )

    @property
    def stats(self):
        return html.Div([dcc.Markdown(children='placeholder', id=self.stats_markdown_id)])

    @property
    def controls(self):
        return dbc.Card(
            [self.interval_dropdown, self.line_checklist, self.interval_slider, self.stats],
            body=True,
        )

    def tab(self, id_, label):
        return dbc.Tab(
            [
                dcc.Graph(id=id_)
            ],
            label=label
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

    #Multi Line
    @property
    def multi_line_interruption(self):
        return dbc.Row([
                self.header,
                dcc.Markdown(markdown.PER_YEAR),
                dbc.Col([
                    dbc.Card(
                        [self.line_checklist, self.interval_slider, self.stats],
                        body=True,
                    )
                ]),
                dbc.Col([
                    dbc.Card(
                        dcc.Tabs([
                            self.tab(
                                self.graph_cumulative_id,
                                label='Frequency'
                                ),
                            self.tab(
                                self.graph_duration_id, 
                                label='Duration'
                                ),
                        ], id='frq_dur_id')
                    )
                ],width=8)
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
                Input(self.checklist_id, 'value'),
            ]
        return out_, in_

    #Per Line
    @property
    def per_line_interruption(self):
        return dbc.Row([
                dcc.Markdown(markdown.PER_LINE),
                dbc.Col([
                    dbc.Card(
                        [self.line_checklist, self.interval_slider, self.stats],
                        body=True,
                    )
                ]),
                dbc.Col([
                    dbc.Card(
                        dcc.Tabs([
                            self.tab(self.graph_duration_id, 'Distribution Throught Year')
                        ])
                    )
                ],width=8)
            ])

    @property
    def per_line_interruption_IO(self):
        out_ = [
                Output(self.graph_duration_id, 'figure'),
                Output(self.stats_markdown_id, 'children'),
            ]
        in_ = [
                Input(self.slider_id, 'value'),
                Input(self.checklist_id, 'value')
            ]
        return out_, in_

    #Per Station
    @property
    def per_station_interruption(self):
        return dbc.Row([
                self.header,
                dcc.Markdown(markdown.PER_STATION),
                dbc.Col([
                    dbc.Card(
                        [self.line_radioItems, self.interval_slider, self.stats],
                        body=True,
                    )
                ]),
                dbc.Col([
                    dbc.Card(
                        dcc.Tabs([
                            self.tab(self.graph_cumulative_id, 'Frequency')
                        ])
                    )
                ],width=8)
            ])

    @property
    def per_station_interruption_IO(self):
        out_ = [
                Output(self.graph_cumulative_id, 'figure'),
                Output(self.stats_markdown_id, 'children'),
            ]
        in_ = [
                Input(self.slider_id, 'value'),
                Input(self.radioItems_id, 'value')
            ]
        return out_, in_

    #Elevator
    @property
    def elevator_interruption(self):
        return dbc.Row([
                self.header,
                dcc.Markdown(markdown.ELEVATOR),
                dbc.Col([
                    dbc.Card(
                        [self.line_checklist, self.interval_slider, self.stats],
                        body=True,
                    )
                ]),
                dbc.Col([
                    dbc.Card(
                        dcc.Tabs([
                            self.tab(self.graph_cumulative_id, 'All Mention'),
                            self.tab(self.graph_duration_id, 'Broken')
                        ])
                    )
                ],width=8)
            ])

    @property
    def elevator_interruption_IO(self):
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

