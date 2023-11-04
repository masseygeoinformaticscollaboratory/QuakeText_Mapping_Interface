import pandas as pd
from pathlib import Path
import chardet
from flair.data import Sentence
from flair.nn import Classifier


def read_data():
    path = 'NPL_Data'
    files = Path(path).glob('*.csv')
    dfs = list()
    for f in files:
        df = pd.read_csv(f, encoding='macroman')
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def clean_data(data):
    data = data.filter([' tweet_text', ' tweet_lon', ' tweet_lat'])
    data = data.dropna(subset=[' tweet_lon', ' tweet_lat'])
    data.rename(columns={' tweet_text': 'tweet_text', ' tweet_lon': 'tweet_lon', ' tweet_lat': 'tweet_lat'},
                inplace=True)
    return data.drop_duplicates()


def perform_ner(data):
    tagger = Classifier.load('ner')
    new_data = pd.DataFrame(columns=['tweet_text', 'location', 'tweet_lat', 'tweet_lon'])
    for index, row in data.iterrows():
        sentence = Sentence(row['tweet_text'])
        tagger.predict(sentence) # This sometimes misses some locations. e.g. 'CA'
        for label in sentence.get_labels():
            if label.value == "LOC":
                new_data = pd.concat([new_data, pd.DataFrame.from_records(
                    [{"tweet_text": row["tweet_text"], "location": label.data_point.text, "tweet_lat": row['tweet_lat'],
                      "tweet_lon": row['tweet_lon']}])])
    new_data.reset_index(drop=True, inplace=True)
    new_data.to_csv("nerNPLDataCleaned.csv", index=False)


def run():
    data = read_data()
    data = clean_data(data)
    perform_ner(data)


run()
