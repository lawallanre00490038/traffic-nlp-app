import dash
from dash import Dash, dcc, html, Input, Output
import os, pandas as pd
import plotly.express as px
from functions.style import dropdown
from functions.functions import filter_by_category


# df = pd.read_csv("datasets/final_data.csv").dropna()
# df["date"] = pd.to_datetime(df["date"])


def filter_categories(app, df):

    layout = html.Div([
        html.H1(children="Select the graph based on the dropdown"),
        
        html.Div([
            dcc.Dropdown(
                id='select_category_for_traffic',
                options=[{'label': x, 'value': x} for x in df.traffic_class.unique()],
                value='free flow',
                style=dropdown()[0]
            )
        ], style={
            'display': 'flex', 
            'justify-content': 'center', 
            'align-items': 'center'
            }
        ),

        dcc.Graph(id='graph-content')
    ])

    @app.callback(
        Output('graph-content', 'figure', allow_duplicate=True),
        Input('select_category_for_traffic', 'value'),
        prevent_initial_call=True
    )
    def update_graph(value):
        dff = filter_by_category(value)
        fig = px.bar(
            dff,
            x="count",
            y="place",
            color="count",
            orientation="h",
            facet_row_spacing=0.2
        )
        fig.update_traces(hovertemplate="<br>".join([
        "Place: %{y}",
        "Count: %{x}"
        ]))

        fig.update_layout(
            xaxis_title='Traffic Category',
            yaxis_title='Count',
            xaxis_tickfont=dict(size=14, color='black'),
            yaxis_tickfont=dict(size=14, color='black'),
            xaxis_title_font=dict(size=16, color='black'),
            yaxis_title_font=dict(size=16, color='black'),
            plot_bgcolor='white',
        )
        return fig
    
    return layout  # added this line to return the layout
