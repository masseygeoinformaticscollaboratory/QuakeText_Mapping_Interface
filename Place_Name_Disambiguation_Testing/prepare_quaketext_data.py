import pandas as pd
from pathlib import Path

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
        columns=['place name', 'tweet text'])
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
    rows = []
    geolocator = GeoNames(username='QuakeText')

    place_entities = get_relations(items, "place name")

    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]
        geonames_instances = geolocator.geocode(place, exactly_one=False)
        for instance in geonames_instances:
            print(instance.raw)
            if instance.address.split(',') == place:
                geonames_string = instance.raw.toponymName + ',' + ',' + instance.raw.countryName + ',' + instance.raw.countryCode + ',' + instance.raw.fcodeName
                rows.append({'place name': place_entity, 'tweet text': tweet, "geonames id": instance.raw.geonameId, })
    return rows


def get_relations(list_of_lists, target):
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
    return relations


# data = read_data()
# data.to_csv('quake_text_prepped_data.csv', index=False)

geolocator = GeoNames(username='QuakeText')

geonames_instances = geolocator.geocode('Pakistan', exactly_one=False)
for instance in geonames_instances:
    geonames_string = instance.raw.get('toponymName') + ', ' + instance.raw.get('countryName') + ', ' + instance.raw.get(
        'countryCode') + ', ' + instance.raw.get('fcodeName')
    print(geonames_string)
