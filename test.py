import pandas as pd

df = pd.read_csv("data/coordinates_data.csv", parse_dates=["date"])

start_date = df.date.min() 

end_date = df.date.max()


def filter_by_date_and_categories(df, category, start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['traffic_class'] == category)
    df = df[mask]
    return df

ans = filter_by_date_and_categories(df, "free flow", start_date, end_date)

print(ans.columns)
