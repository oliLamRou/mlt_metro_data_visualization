import numpy as np

from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.dashboard_section import DashboardSection
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS


color_discrete_map = {
                 "rem_infoservice": "rgb(126,175,0)",
                 "stm_orange": "rgb(237,106,0)",
                 "stm_verte": "rgb(0,128,52)",
                 "stm_bleue": "rgb(0,98,185)",
                 "stm_jaune": "rgb(255,204,0)",
             }

"""
1. Yearly line comparison. Tab for "day with interruption" & "duration"
    Only choice of line + years range

2. Need to chose a line, then one line per year. tab for "day with interruption" & "duration"
    


"""

#Data
"""
- Amount of Day with at least 1 Interruption of service, line chart with all lines with proper color
- Duration of Interruption
- Elevator Down
- Per Station Interruption
- interruption vs achalandage 
"""

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

#Multi Line
def multi_line_interruption_callback(ds):
    @app.callback(ds.multi_line_interruption_IO[0], ds.multi_line_interruption_IO[1])
    def interruption_amount_callback(year_range, lines):
        ds.filtered_lines = lines
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[1]
        yticks_stop = list(range(0, ds.grouped_df.stop.astype(int).max()+5, 5))
        yticks_duration = list(range(0, ds.grouped_df.duration.astype(int).max()+500, 500))

        fig1 = px.line(
            ds.slice_df,
            x='interval', 
            y='stop', 
            color='line', 
            title='Number of day with 1 or more interruption',
            color_discrete_map=color_discrete_map
        ).update_layout(
            xaxis_title="Date", 
            yaxis_title="amount of time",
            xaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.interval.astype(int),
                ticktext = ds.slice_df.interval.astype(str),
            ),
            yaxis = dict(
                tickmode = 'array',
                tickvals = yticks_stop,
                ticktext = yticks_stop,
            )
        )
        fig2 = px.line(
            ds.slice_df, 
            x='interval', 
            y='duration', 
            color='line', 
            title='Total duration time',
            color_discrete_map=color_discrete_map
        ).update_layout(
            xaxis_title="Date", 
            yaxis_title="Minute",
            xaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.interval.astype(int),
                ticktext = ds.slice_df.interval.astype(str),
            ),
            yaxis = dict(
                tickmode = 'array',
                tickvals = yticks_duration,
                ticktext = yticks_duration,
            )

        )
        # stats = ds.update_stats()
        stats = ''

        return [fig1, fig2, stats]

mutli_line_interruption = DashboardSection(
        namespace = 'multi_interruption',
        title = 'Comparative between lines',
        interval = 'year'
    )
multi_line_interruption_callback(mutli_line_interruption)


#per Line
def per_line_interruption_callback(ds):
    @app.callback(ds.per_line_interruption_IO[0], ds.per_line_interruption_IO[1])
    def interruption_amount_callback(year_range, lines):
        ds.filtered_lines = lines
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[1]

        fig1 = px.scatter(
            ds.slice_df, 
            x='interval', 
            y='range', 
            color='line',
            size='duration',
            title='Total duration time',
            color_discrete_map=color_discrete_map
        ).update_layout(
            xaxis_title="Day Of The Year", 
            yaxis_title="Year",
            yaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.range.astype(int),
                ticktext = ds.slice_df.range.astype(str),
            )             
        )
        # stats = ds.update_stats()
        stats = ''

        return [fig1, stats]

per_line_interruption = DashboardSection(
        namespace = 'per_line_interruption',
        title = 'Per Line',
        interval = 'day'
    )
per_line_interruption_callback(per_line_interruption)

#per Station
def per_station_interruption_callback(ds):
    @app.callback(ds.per_station_interruption_IO[0], ds.per_station_interruption_IO[1])
    def interruption_amount_callback(year_range, line):
        ds.filtered_lines = [line]
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[1]
        data = ds.slice_df[['interval'] + list(LINES_STATIONS[line].keys())]
        data.set_index('interval', inplace=True)

        fig1 = px.imshow(
                data,
                color_continuous_scale = 'Hot',
        ).update_layout(
            yaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.interval.astype(int),
                ticktext = ds.slice_df.interval.astype(str),
            )    
        )

        # stats = ds.update_stats()
        stats = ''

        return [fig1, stats]

per_station_interruption = DashboardSection(
        namespace = 'per_station_interruption',
        title = 'Per Station',
        interval = 'year'
    )
per_station_interruption_callback(per_station_interruption)

if __name__ == '__main__':
    app.layout = dbc.Container(
    [
        dcc.Markdown("# Analysis of STM and REM lines"),
        dcc.Markdown("""
            - Data from twitter that goes back to 2013.  
            - The Rem is a new line that is automated and has screen door at each station.  
            - Let's see which line has the most interruption and if there is a pettern or not.  
            """),
        mutli_line_interruption.multi_line_interruption,
        dcc.Markdown("### Single Line Analysis"),
        dcc.Markdown("## Interruptions Of Service"),
        per_line_interruption.per_line_interruption,
        dcc.Markdown("### Single Line Analysis"),
        dcc.Markdown("## Interruptions Of Service"),
        per_station_interruption.per_station_interruption,        
    ],
    fluid=True,
    )

    app.run(debug=True)


