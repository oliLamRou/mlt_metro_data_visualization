import numpy as np
import math

from dash import Dash, html, ctx, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.dashboard_section import DashboardSection
from mtl_metro_data_visualization.dashboard import markdown
from mtl_metro_data_visualization.constant._lines_stations import LINES_STATIONS
from mtl_metro_data_visualization.constant._lines_stations import LINES_COLOR

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
            title='Amount of days with 1 or more interruption',
            color_discrete_map=LINES_COLOR
        ).update_layout(
            xaxis_title="Year", 
            yaxis_title="Amount of Days",
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
            title='Duration total per year',
            color_discrete_map=LINES_COLOR
        ).update_layout(
            xaxis_title="Year", 
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
        stats = f"""
        ###### Frequency
        - Average: {round(ds.slice_df['stop'].mean(), 1)} 
        - Max: {round(ds.slice_df['stop'].max(), 1)}
        ###### Duration
        - Average: {round(ds.slice_df['duration'].mean(), 1)}
        - Max: {round(ds.slice_df['duration'].max(), 1)}
        """

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
            title='Duration per day',
            color_discrete_map=LINES_COLOR
        ).update_layout(
            xaxis_title="Day of the year", 
            yaxis_title="Year",
            yaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.range.astype(int),
                ticktext = ds.slice_df.range.astype(str),
            )             
        )
        stats = f"""
        ###### Duration
        - Average: {round(ds.slice_df['duration'].mean(), 1)} 
        - Max: {round(ds.slice_df['duration'].max(), 1)}
        """
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
                title='Amount of interruption per station per year'
        ).update_layout(
            yaxis = dict(
                tickmode = 'array',
                tickvals = ds.slice_df.interval.astype(int),
                ticktext = ds.slice_df.interval.astype(str),
            )    
        )

        top3 = data.mean().sort_values()[-3:].sort_values(ascending=False)
        stats = f"""
        ###### Top 3 Station (average)
        1. {top3.index[0].capitalize()}: {round(top3[0], 2)}
        2. {top3.index[1].capitalize()}: {round(top3[1], 2)}
        3. {top3.index[2].capitalize()}: {round(top3[2], 2)}
        """
        return [fig1, stats]

per_station_interruption = DashboardSection(
        namespace = 'per_station_interruption',
        title = 'Per Station',
        interval = 'year'
    )
per_station_interruption_callback(per_station_interruption)

#REM Elevator
def elevator_interruption_callback(ds):
    @app.callback(ds.elevator_interruption_IO[0], ds.elevator_interruption_IO[1])
    def interruption_elevator_callback(year_range, line):
        ds.filtered_lines = line
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[-1]

        fig1 = px.line(
            ds.slice_df, 
            x='interval', 
            y='elevator',
            color='line',
            title='Duration per day',
            color_discrete_map=LINES_COLOR
        ).update_layout(
            xaxis_title="Month", 
            yaxis_title="Days",
            yaxis = dict(
                tickmode = 'array',
                tickvals = [days for days in range(0, (math.ceil(ds.slice_df.elevator.max() / 10) * 10 ) + 1, 5)],
                ticktext = [str(days) for days in range(0, (math.ceil(ds.slice_df.elevator.max() / 10) * 10 ) + 1, 5)]
            )             
        )

        fig2 = px.line(
            ds.slice_df, 
            x='interval', 
            y='elevator_closed',
            color='line',
            title='Duration per day',
            color_discrete_map=LINES_COLOR
        ).update_layout(
            xaxis_title="Month", 
            yaxis_title="Days",
            yaxis = dict(
                tickmode = 'array',
                tickvals = [days for days in range(0, (math.ceil(ds.slice_df.elevator.max() / 10) * 10 ) + 1, 5)],
                ticktext = [str(days) for days in range(0, (math.ceil(ds.slice_df.elevator.max() / 10) * 10 ) + 1, 5)]
            )             
        )
        stats = f"""
        ###### Frequency
        - Average: {round(ds.slice_df['elevator'].mean(), 1)} 
        - Max: {round(ds.slice_df['elevator'].max(), 1)}
        ###### Duration
        - Average: {round(ds.slice_df['elevator_closed'].mean(), 1)}
        - Max: {round(ds.slice_df['elevator_closed'].max(), 1)}
        """

        return [fig1, fig2, stats]

elevator_interruption = DashboardSection(
        namespace = 'elevator_interruption',
        title = 'Elevator',
        interval = 'year'
    )
elevator_interruption_callback(elevator_interruption)

if __name__ == '__main__':
    app.layout = dbc.Container(
    [
        dcc.Markdown(markdown.INTRO, style={'width': '80%'}),
        mutli_line_interruption.multi_line_interruption,
        per_line_interruption.per_line_interruption,
        per_station_interruption.per_station_interruption,
        elevator_interruption.elevator_interruption,
        dcc.Markdown(markdown.CONCLUSION, style={'width': '80%'})
    ],
    fluid=True,
    )

    app.run(debug=True)