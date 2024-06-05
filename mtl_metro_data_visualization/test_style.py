import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start="2021-01-01", periods=10, freq='D'),
    "Value": [10, 15, 13, 17, 20, 23, 21, 25, 22, 30]
})

# Create a line chart
fig = px.line(df, x="Date", y="Value", title="Sample Line Chart")

# Initialize the app with the DARKLY theme
app = dash.Dash(__name__)

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("My Dashboard", className='text-center text-light mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='example-graph', figure=fig), width=12)
    ]),
    dcc.RangeSlider(
        min=2020,
        max=2022,
        step=1,
        value=[2020, 2022],
        marks={2020: '', 2021: '', 2022: ''},
    ),
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
