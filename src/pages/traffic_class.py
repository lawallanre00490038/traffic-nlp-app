import dash
from dash import Dash, dcc, html, Input, Output, callback
import os, pandas as pd
import plotly.express as px
from functions.style import graph_style, dropdown
from components.filter_category import filter_categories
from functions.functions import filter_by_category

dash.register_page(__name__, path="/class")

from functions.get_file import get_pandas_data
from pathlib import Path
DATA_PATH = Path(os.path.abspath(__file__)).parent.parent.parent / 'data'
df = pd.read_csv(DATA_PATH  / "final_data.csv").dropna()
df["date"] = pd.to_datetime(df["date"])

# Main traffic classs
data = df.groupby(['traffic_class']).size().reset_index(name='count').sort_values(by='count', ascending=False).reset_index(drop=True)
data_bar = px.bar(data, x='traffic_class', y='count', color='traffic_class')
data_bar.update_layout(
    title='Total Traffic Occurrences in Dataset',
    xaxis_title='Traffic Classes',
    yaxis_title='Count',
    xaxis_tickangle=-45,
    yaxis_tickangle=-45,
    xaxis_tickfont=dict(size=14, color='black'),
    yaxis_tickfont=dict(size=14, color='black'),
    xaxis_title_font=dict(size=16, color='black'),
    yaxis_title_font=dict(size=16, color='black'),
    plot_bgcolor='white',
)


layout =  html.Div(
    [
        # First Graph Child
        html.H1("Traffic Data Insights"),
        
        html.Div(dcc.Graph(id="unique_classes", figure=data_bar,style=graph_style()[0])),

        html.Div([
        html.H1(children="Choose a trafffic category from the dropdown menu to visualize different aspects of traffic data"),
        
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
    ],style=graph_style()[0])

    ],
    style={
        'textAlign': 'center', 
        'width': '90%', 
        'margin': '0 auto'
    }
)


@dash.callback(
    Output('graph-content', 'figure', allow_duplicate=True),
    Input('select_category_for_traffic', 'value'),
    prevent_initial_call=True
)
def update_graph(value):
    category = "free flow"
    if value:
        category = value
    df = df.copy(deep=True)
    dff = filter_by_category(category, df)
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