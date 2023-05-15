import dash
from dash import Dash, dcc, html, Input, Output, callback

dash.register_page(__name__, path="/about")

# Define the layout for the traffic page
layout = html.Div([
    html.H1('About Page'),
    # Add other components for your traffic page here
])
    
