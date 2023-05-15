import dash
from dash import Dash, dcc, html, Input, Output, callback
from functions.get_file import get_pandas_data

dash.register_page(__name__, path="/")

layout = html.Div([
    html.Div(className="hero", children=[
        html.Div(className="hero-overlay", children=[
            html.Div(className="hero-content", children=[
                html.H1("Traffic Analysis", className="hero-title"),
                html.P("Real-time traffic data at your fingertips", className="hero-subtitle")
            ])
        ]),
        html.Div(className="hero-image")
    ])
])
