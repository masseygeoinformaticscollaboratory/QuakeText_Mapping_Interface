import pandas as pd


def combine_columns(row):
    parts = [str(row['verbatimLocality']), str(row['habitat']), str(row['eventRemarks'])]
    non_nan_parts = [part for part in parts if part != 'nan']
    return ' '.join(non_nan_parts)


def clean_data(data_frame):
    data_frame = data_frame.filter(['text', 'decimalLatitude', 'decimalLongitude'])
    data_frame = data_frame[data_frame['decimalLatitude'].notna() & data_frame['decimalLongitude'].notna()]
    data_frame.rename(columns={'decimalLongitude': 'Longitude', 'decimalLatitude': 'Latitude'},
                      inplace=True)
    return data_frame.drop_duplicates()


data = pd.read_csv('dataset1.csv', low_memory=False)
data['text'] = data.apply(combine_columns, axis=1)

data = clean_data(data)
data.to_csv("output.csv", index=False)
