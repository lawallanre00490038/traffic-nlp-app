import pathlib
import pandas as pd 
from functions.get_file import get_pandas_data
def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   '''
   Load data from /data directory as a pandas DataFrame
   using relative paths. Relative paths are necessary for
   data loading to work in Heroku.
   '''
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))



# PATH = pathlib.Path(__file__)
# DATA_PATH = PATH.joinpath("data").resolve()

# df = pd.read_csv(DATA_PATH.joinpath("final_data.csv")).dropna()
# print(PATH)
# print(DATA_PATH)
# print(get_pandas_data("final_data.csv"))

import os
import pathlib
from pathlib import Path
# Get the root directory path
DATA_PATH = pathlib.Path(os.path.abspath(__file__)).parent.parent / 'data'

CSV_FILE_PATH = DATA_PATH / 'final_data.csv'

print(pd.read_csv(CSV_FILE_PATH))
