from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.dashboard_section import DashboardSection


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
"""

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])


def multi_line_interruption_callback(ds, col):
    @app.callback(ds.multi_line_interruption_IO[0], ds.multi_line_interruption_IO[1])
    def interruption_amount_callback(year_range, lines):
        ds.filtered_lines = lines
        ds.filtered_start = year_range[0]
        ds.filtered_end = year_range[1]

        fig1 = px.line(
            ds.year_range, 
            x='date', 
            y=col, 
            color='line', 
            title='Number of day with 1 or more interruption'
        ).update_layout(
            xaxis_title="Date", yaxis_title="amount of time"
        )
        fig2 = px.line(
            ds.filtered_df, 
            x='date', 
            y=col, 
            color='line', 
            title='Total duration time'
        ).update_layout(
            xaxis_title="Date", yaxis_title="Minute"
        )
        stats = ds.update_stats()

        return [fig1, fig2, stats]

#Multi Line
mutli_line_interruption = DashboardSection(
        namespace = 'multi_interruption',
        title = 'Comparative between lines',
        column = 'stop',
        daily_grouping_func = max,
        interval_grouping_func = sum,
        interval = 'year'
    )
multi_line_interruption_callback(mutli_line_interruption, 'stop')


# def _callback(ds, col):
#     @app.callback(ds.IO[0], ds.IO[1])
#     def interruption_amount_callback(year_range, lines, interval):
#         df = ds.grouped_df
#         if ctx.triggered_id == ds.dropdown_id:
#             df = ds.update_interval(interval)

#         ds.filtered_lines = lines
#         ds.filtered_start = year_range[0]
#         ds.filtered_end = year_range[1]

#         if interval in ['month', 'weekday']:
#             fig = px.bar(ds.filtered_df, x='date', y=col, color='line')
#         else:
#             fig = px.line(ds.filtered_df, x='date', y=col, color='line')

#         fig.update_layout(showlegend=False)

#         stats = ds.update_stats()

#         return [fig, stats]


# #Cumulative
# interruption_amount = DashboardSection(
#         namespace = 'interruption',
#         title = 'Cumulative',
#         column = 'stop',
#         daily_grouping_func = max,
#         interval_grouping_func = sum,
#         interval = 'year'    
#     )
# _callback(interruption_amount, 'stop')

# #Duration
# interruption_duration = DashboardSection(
#         namespace = 'duration',
#         title = 'Duration in Minute',
#         column = 'duration',
#         daily_grouping_func = sum,
#         interval_grouping_func = sum,
#         interval = 'year'    
#     )
# _callback(interruption_duration, 'duration')

# #Duration
# elevator = DashboardSection(
#         namespace = 'elevator',
#         title = 'Cumulative',
#         column = 'elevator',
#         daily_grouping_func = max,
#         interval_grouping_func = sum,
#         interval = 'year'    
#     )
# _callback(elevator, 'elevator')

if __name__ == '__main__':
    app.layout = dbc.Container(
    [
        dcc.Markdown("# Interruption of Service"),
        dcc.Markdown("bullet pointe of some finding"),
        mutli_line_interruption.multi_line_interruption,
        # dcc.Markdown("### Single Line Analysis"),
        # dcc.Markdown("## Interruptions Of Service"),
        # interruption_amount.interruption,
        # interruption_duration.interruption,
        # dcc.Markdown("## Elevators Problems"),
        # elevator.interruption,
    ],
    fluid=True,
    )

    app.run(debug=True)


