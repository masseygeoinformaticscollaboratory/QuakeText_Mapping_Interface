from pathlib import Path

import pandas as pd
from geopy import GeoNames

count = 0


def read_data():
    print("Reading files...")
    path = '../Backend/dataFiles'
    files = Path(path).glob('*.json')
    dfs = list()
    for f in files:
        current_data = pd.read_json(f)
        dfs.append(current_data)

    return clean_df(pd.concat(dfs, ignore_index=True))


def clean_df(data_frame: pd.DataFrame):
    print("Cleaning Data...")
    relations_list = data_frame.get("relations")
    tweets = data_frame.get("tweet")
    entity_list = data_frame.get("entities")
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


def get_database_rows(items, tweet):
    global count
    rows = []
    geolocator_1 = GeoNames(username='QuakeText')
    geolocator_2 = GeoNames(username='20004521_lp')
    geolocator_3 = GeoNames(username='lp_20004521')
    geolocator_4 = GeoNames(username='lp_776')

    place_entities = get_relations(items, "place name")

    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]

        if count < 900:
            get_instance(geolocator_1, place_entity, rows, tweet)
            count += 1
        elif 899 < count < 1799:
            get_instance(geolocator_2, place_entity, rows, tweet)
            count += 1
        elif 1799 < count < 2399:
            get_instance(geolocator_3, place_entity, rows, tweet)
            count += 1
        else:
            get_instance(geolocator_4, place_entity, rows, tweet)
            count += 1

        print(count)

    return rows


def get_instance(geolocator_1, place_entity, rows, tweet):
    geonames_instances = geolocator_1.geocode(place_entity, exactly_one=False, timeout=None)
    if geonames_instances is not None:
        for instance in geonames_instances:
            if instance.address.split(',')[0].lower() == place_entity.lower():
                geonames_list = [instance.raw.get('toponymName'), instance.raw.get('countryName'),
                                 instance.raw.get(
                                     'countryCode'), instance.raw.get('fcodeName')]
                cleaned_geonames_list = [item for item in geonames_list if item is not None]

                geonames_string = ', '.join(cleaned_geonames_list)

                rows.append(
                    {'place name': place_entity, 'tweet text': tweet,
                     "geonames id": instance.raw.get('geonameId'), 'geonames string': geonames_string})


def get_relations(list_of_lists, target):
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
    return relations


data = read_data()
data.to_csv('quake_text_prepped_data.csv', index=False)
