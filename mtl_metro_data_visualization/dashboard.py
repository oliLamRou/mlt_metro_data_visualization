from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from mtl_metro_data_visualization.dashboard.lines_graph import LinesGraph

#Data
"""
- Amount of Day with at least 1 Interruption of service, line chart with all lines with proper color
- Duration of Interruption
- Elevator Down
- Per Station Interruption
"""
lines_graph = LinesGraph(
        namespace = 'interruption',
        columns = ['stop', 'slow'],
        daily_grouping_func = max,
        interval_grouping_func = sum,
        interval = 'year'    
    )
# lines_graph = LinesGraph(interruptions)
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

@app.callback(lines_graph.IO[0], lines_graph.IO[1])
def filter_on_current(year_range, lines, interval):
    df = lines_graph.grouped_df
    if ctx.triggered_id == lines_graph.dropdown_id:
        df = lines_graph.update_interval(interval)

    df_ = df[df.line.isin(lines)]
    df_ = lines_graph.year_range(df_, year_range[0], year_range[1])
    fig = px.line(df_, x='date', y='stop', color='line')
    fig.update_layout(showlegend=False)
    return fig

if __name__ == '__main__':
    app.layout = dbc.Container(
    [
        lines_graph.interruption,
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
    )

    app.run(debug=True)


