# def filter_by_category_and_date(category, start_date, end_date):
#         import pandas as pd
#         df = pd.read_csv("./datasets/final_data.csv").dropna()
#         df["date"] = pd.to_datetime(df["date"])
        
#         mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['traffic_class'] == category)
#         df_filtered = df.loc[mask].groupby(["place", "date"]).size().reset_index(name='count').sort_values(by='count', ascending=True).reset_index(drop=True)
#         return df_filtered.tail(20)



def filter_by_date_and_category(df, category, start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['traffic_class'] == category)
    df = df[mask]
    return df


def filter_by_category(category, df):
      data = df[(df['traffic_class'] == category) & (~df['place'].str.contains("Tanker"))]
      df_filtered = data.groupby(["place"]).size().reset_index(name='count').sort_values(by='count', ascending=False).reset_index(drop=True)
      return df_filtered.head(20)[::-1]



import re
from datetime import datetime

# Assuming you have a DataFrame named 'df' with a 'date' column

# Define a function to extract date and time from a given date string
def extract_date_and_time(date_time):
    # Extract the date component
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', date_time)
    date_str = date_match.group(1)
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Extract the time component
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', date_time)
    time_str = time_match.group()
    time = datetime.strptime(time_str, '%H:%M:%S').time()

    return date, time