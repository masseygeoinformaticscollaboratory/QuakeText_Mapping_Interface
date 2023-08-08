import pandas as pd
from flair.nn import Classifier
from flair.data import Sentence


def combine_columns(row):
    parts = [str(row['verbatimLocality']), str(row['habitat']), str(row['eventRemarks'])]
    non_nan_parts = [part for part in parts if part != 'nan']
    return ' '.join(non_nan_parts)


def clean_data(data_frame):
    data_frame['text'] = data_frame.apply(combine_columns, axis=1)
    data_frame = data_frame.filter(['text', 'decimalLatitude', 'decimalLongitude'])
    data_frame = data_frame[data_frame['decimalLatitude'].notna() & data_frame['decimalLongitude'].notna()]
    data_frame.rename(columns={'decimalLongitude': 'Longitude', 'decimalLatitude': 'Latitude'},
                      inplace=True)
    return data_frame.drop_duplicates()


def perform_ner(data):
    tagger = Classifier.load('ner')
    new_data = pd.DataFrame(columns=['text', 'location', 'text_latitude', 'text_longitude'])
    for index, row in data.iterrows():
        sentence = Sentence(row['text'])
        tagger.predict(sentence)
        for label in sentence.get_labels():
            if label.value == "LOC":
                new_data = pd.concat(
                    [new_data, pd.DataFrame.from_records([{"text": row["text"], "location": label.data_point.text,
                                                           "text_latitude": row['Latitude'],
                                                           "text_longitude": row['Longitude']}])])
    new_data.reset_index(drop=True, inplace=True)
    new_data.to_csv("nerDataCleaned.csv", index=False)


def run():
    data = pd.read_csv('dataset1.csv', low_memory=False)
    data = clean_data(data)
    perform_ner(data)


run()
