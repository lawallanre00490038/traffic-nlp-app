import pandas as pd
import dash, os
from dash import Dash, dcc, html, Input, Output, callback
from dash import  dash_table
from dash.dash_table.Format import Group
from dateutil import tz
from functions.style import style_table
from functions.get_file import get_pandas_data, get_txt_data
from pathlib import Path
DATA_PATH = Path(os.path.abspath(__file__)).parent.parent.parent / 'data'
DATA_TXT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent / 'data'

dash.register_page(__name__, path="/data")

table_extracted = pd.read_csv(DATA_TXT_PATH /"selected_data.txt", header=0, sep='\t')
table_extracted = table_extracted.copy(deep=True)
table_extracted['date'] = pd.to_datetime(table_extracted['date']).apply(lambda x: x.astimezone(tz.gettz('UTC')).replace(tzinfo=None))


df = pd.read_csv(DATA_PATH  / "final_data.csv").dropna()
df["date"] = pd.to_datetime(df["date"])
df = df.drop(columns=["Unnamed: 0"])
df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.astimezone(tz.gettz('UTC')).replace(tzinfo=None))

layout = html.Div([

    html.Div(
        [
            html.H1('Cleaned Extracted Data'),
            dash_table.DataTable(
                id='table_extracted',
                columns=[{"name": i, "id": i} for i in table_extracted.columns],
                data=table_extracted.to_dict('records'),
                filter_action='native',
                page_size=10,
                style_table=style_table()[0],
                style_header=style_table()[1],
                style_cell=style_table()[2]
            )
        ]
    ),
    html.Div([
        html.H1('Processed Data'),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=df['date'].min(),
            max_date_allowed=df['date'].max(),
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            style={
                'margin': '10px 0px'
            }
        ),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            filter_action='native',
            page_size=10,
            style_table=style_table()[0],
            style_header=style_table()[1],
            style_cell=style_table()[2]
        )
])
    
], style={
        'width': '80%',
        'margin': '0 auto'
    })

@dash.callback(
    Output('table', 'data'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_table(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df.to_dict('records')
