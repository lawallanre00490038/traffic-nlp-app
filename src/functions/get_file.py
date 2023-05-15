from pathlib import Path
import pandas as pd
import os

def get_pandas_data(csv_filename):
   '''
   Load data from /data directory as a pandas DataFrame
   using relative paths. Relative paths are necessary for
   data loading to work in Heroku.
   '''
   # PATH = Path(__file__)
   # DATA_PATH = PATH.joinpath("data").resolve()

      # Get the root directory path
   ROOT_PATH = Path(os.path.abspath(__file__)).parent

   # Path to the data folder
   DATA_PATH = ROOT_PATH / 'data'

   # Path to the CSV file
   CSV_FILE_PATH = DATA_PATH / csv_filename

   return pd.read_csv(CSV_FILE_PATH)



def get_txt_data(txt_filename: str) -> pd.DataFrame:
   '''
   Load data from /data directory as a pandas DataFrame
   using relative paths. Relative paths are necessary for
   data loading to work in Heroku.
   '''
   PATH = Path(__file__).parent
   DATA_PATH = PATH.joinpath("data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(txt_filename), header=0, sep='\t')