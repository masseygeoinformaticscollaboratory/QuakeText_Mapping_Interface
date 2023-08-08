from flair.models import SequenceTagger
from geopy.geocoders import GeoNames

import pandas as pd
from flair.data import Sentence


def get_coordinates():
    geolocator = GeoNames(username='QuakeText')  # Replace with your GeoNames username

    place_name = "Balochistan"
    geonames_instances = geolocator.geocode(place_name, exactly_one=False)

    for instance in geonames_instances:
        hello = instance.raw
        print(instance.raw.get('fclName'))


def perform_ner(data):
    # Load the Flair NER tagger
    tagger = SequenceTagger.load('ner')

    # Assuming 'data' is your original DataFrame
    new_data_list = []

    for index, row in data.iterrows():
        sentence = Sentence(row['text'])
        tagger.predict(sentence)

        for label in sentence.get_labels():
            if label.value == "LOC":
                new_data_list.append({
                    "text": row["text"],
                    "location": label.data_point.text,
                    "text_latitude": row['Latitude'],
                    "text_longitude": row['Longitude']
                })

    # Create the new DataFrame from the list of dictionaries
    new_data = pd.DataFrame.from_records(new_data_list)
    new_data.reset_index(drop=True, inplace=True)
    new_data.to_csv("testCleaned.csv", index=False)


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


def run():
    data = pd.read_csv('dataset1.csv', low_memory=False)
    data = clean_data(data)
    perform_ner(data)


run()
