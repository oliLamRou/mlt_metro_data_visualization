from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.dashboard_section import DashboardSection

#Data
"""
- Amount of Day with at least 1 Interruption of service, line chart with all lines with proper color
- Duration of Interruption
- Elevator Down
- Per Station Interruption
"""

def _callback(ds, col):
    @app.callback(ds.IO[0], ds.IO[1])
    def interruption_amount_callback(year_range, lines, interval):
        df = ds.grouped_df
        if ctx.triggered_id == ds.dropdown_id:
            df = ds.update_interval(interval)

        ds.filtered_lines = lines
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[1]

        fig = px.line(ds.filtered_df, x='date', y=col, color='line')
        fig.update_layout(showlegend=False)

        stats = ds.update_stats()

        return [fig, stats]

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


#Cumulative
interruption_amount = DashboardSection(
        namespace = 'interruption',
        title = 'Cumulative',
        column = 'stop',
        daily_grouping_func = max,
        interval_grouping_func = sum,
        interval = 'year'    
    )
_callback(interruption_amount, 'stop')

#Duration
interruption_duration = DashboardSection(
        namespace = 'duration',
        title = 'Duration in Minute',
        column = 'duration',
        daily_grouping_func = sum,
        interval_grouping_func = sum,
        interval = 'year'    
    )
_callback(interruption_duration, 'duration')

#Duration
elevator = DashboardSection(
        namespace = 'elevator',
        title = 'Cumulative',
        column = 'elevator',
        daily_grouping_func = max,
        interval_grouping_func = sum,
        interval = 'year'    
    )
_callback(elevator, 'elevator')

if __name__ == '__main__':
    app.layout = dbc.Container(
    [
        dcc.Markdown("### have some bullet point / summary here"),
        dcc.Markdown("## Interruptions Of Service"),
        interruption_amount.interruption,
        interruption_duration.interruption,
        dcc.Markdown("## Elevators Problems"),
        elevator.interruption,
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
    )

    app.run(debug=True)


