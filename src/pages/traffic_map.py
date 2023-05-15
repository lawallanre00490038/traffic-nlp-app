import dash
from dash import Dash, dcc, html, Input, Output, callback
import os, pandas as pd
from functions.style import dropdown
from functions.functions import filter_by_category,filter_by_date_and_category
from functions.get_data_with_coordinates import get_location
import gmaps
import plotly.express as px

dash.register_page(__name__, path="/map")

from functions.get_file import get_pandas_data
from pathlib import Path
DATA_PATH = Path(os.path.abspath(__file__)).parent.parent.parent / 'data'
df = pd.read_csv(DATA_PATH  / "coordinates_data.csv").dropna()
df["date"] = pd.to_datetime(df["date"])

# Set the API key
gmaps.configure(api_key='AIzaSyDxTCeIB_-YadQbWqDbCSBKtfttEWbF_8w')


layout = html.Div([
    html.H2("Explore different types of traffic incidents on the map by selecting a value from the dropdown menu. See the distribution and location of accidents, free flow traffic, heavy traffic, and breakdowns, and gain valuable insights into traffic patterns and congestion hotspots"),
    html.Div([
        dcc.Dropdown(
            id='map-dropdown-selection',
            options=[{'label': x, 'value': x} for x in df.traffic_class.unique()],
            style=dropdown()[0],
            value="free flow"
        ),
        dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df["date"].min(),
        max_date_allowed=df["date"].max(),
        initial_visible_month=df["date"].min(),
        start_date=df["date"].min(),
        end_date=df["date"].max()
    )
    ], style={
        'display': 'flex', 
        'justifyContent': 'center',
        'columnGap' : '10px',
        'height': '70px',
        'margin': '5px 0px'
        }),
    html.Br(),
    dcc.Graph(id='display_map'),

],
    style={
        'textAlign': 'center', 
        'width': '90%', 
        'margin': '0 auto',
        'height': '60%'
        
    }
)

@dash.callback(
    Output(component_id='display_map',component_property='figure'),
    Input(component_id='map-dropdown-selection', component_property='value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_output_div(value, start_date, end_date):
    fig = None
    if value:
        data = df.copy(deep=True)
        data = filter_by_date_and_category(data, value, start_date, end_date)
        fig = px.scatter_mapbox(
            data, lat="lat", lon="lng", 
            hover_data=["date", "place"],
            zoom=10, height=500,
            color_continuous_scale="Viridis",
            center={"lat": data['lat'].mean(), "lon": data['lng'].mean()}, 
            size=list(range(len(data))), color="place"
        )
        
        fig.update_layout(mapbox_style="open-street-map")

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig if fig is not None else {}



# , hover_name="place", hover_data=["date", "place"]