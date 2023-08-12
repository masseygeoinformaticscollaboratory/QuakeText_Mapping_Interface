import pandas as pd
from pathlib import Path
import time

from geopy import GeoNames


def read_data():
    print("Reading files...")
    path = '../Backend/dataFiles'
    files = Path(path).glob('*.json')
    dfs = list()
    for f in files:
        data = pd.read_json(f)
        dfs.append(data)

    return clean_df(pd.concat(dfs, ignore_index=True))


def clean_df(data: pd.DataFrame):
    print("Cleaing Data...")
    relations_list = data.get("relations")
    tweets = data.get("tweet")
    entity_list = data.get("entities")
    entity_relations = entity_list + relations_list

    # creates empty dataframe to append data
    df = pd.DataFrame(
        columns=['place name', 'tweet text', 'geonames id', 'geonames string'])
    i = 0
    for items in entity_relations:
        [tweet] = tweets[i]
        for row in get_database_rows(items, tweet):
            df = pd.concat([df, pd.DataFrame.from_records([row])])
        i += 1

    df.dropna(inplace=True)
    df = df.drop_duplicates()

    df.reset_index(drop=True, inplace=True)
    return df


count = 0


def get_database_rows(items, tweet):
    global count
    rows = []

    place_entities = get_relations(items, "place name")
    geolocator = GeoNames(username='QuakeText')

    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]
        if count >= 1000:
            count = 0
            sleep_duration = 70 * 60  # 70 minutes * 60 seconds
            time.sleep(sleep_duration)
        else:
            geonames_instances = geolocator.geocode(place_entity, exactly_one=False)
            count += 1
            if geonames_instances is not None:
                for instance in geonames_instances:
                    if instance.address.split(',')[0].lower() == place_entity.lower():
                        geonames_list = [instance.raw.get('toponymName'), instance.raw.get('countryName'),
                                         instance.raw.get(
                                             'countryCode'), instance.raw.get('fcodeName'),
                                         instance.raw.get('fcodeName')]
                        cleaned_geonames_list = [item for item in geonames_list if item is not None]

                        geonames_string = ', '.join(cleaned_geonames_list)

                        rows.append(
                            {'place name': place_entity, 'tweet text': tweet,
                             "geonames id": instance.raw.get('geonameId'), 'geonames string': geonames_string})

    return rows


def get_relations(list_of_lists, target):
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
    return relations


data = read_data()
data.to_csv('quake_text_prepped_data.csv', index=False)
