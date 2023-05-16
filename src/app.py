import dash
from dash import Dash, dcc, html, Input, Output
import os
import plotly.express as px
import os, pandas as pd
from functions.get_file import get_pandas_data
from pathlib import Path

DATA_PATH = Path(os.path.abspath(__file__)).parent.parent / 'data'
df = pd.read_csv(DATA_PATH  / "final_data.csv").dropna()
df["date"] = pd.to_datetime(df["date"])


app = Dash(__name__,
            use_pages=True, 
            pages_folder="pages",
            external_stylesheets=["./static/style.css"],
            suppress_callback_exceptions=True)
server = app.server


app.layout = html.Div(
    [
        html.Div(
        [   
            html.Div([
                html.H2('Lagos Traffic Data Geo-visualization')
                # html.Div(id='marquee-container', children=[
                #     html.P((text for text in ['Hello', 'World', 'How', 'Are', 'You']), className='.marquee')
                # ])
            ]),
            html.Img(src='assets/traffic_logo1.png')
            
        ],  className='logo_title'),

        html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["path"]
                )
            )
            for page in dash.page_registry.values()
        ],  className='nav'),

        dash.page_container,
    ],

    className='header'

    # html.Div(
    #     "This is a footer",
    #     className="footer",
    #     style={'backgroundColor': 'black', 'height':'40px'}
    # )
)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port)
