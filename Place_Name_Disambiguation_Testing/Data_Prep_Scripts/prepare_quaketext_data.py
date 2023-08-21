from pathlib import Path
import numpy as np
import pandas as pd


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
    country_info = pd.read_csv("local_data_base_test/countryInfo.csv", low_memory=False)
    country_info = country_info[['ISO', 'Country', 'Continent']]
    feature_codes = pd.read_csv("local_data_base_test/featureCodes.csv", low_memory=False)
    geonames = pd.read_csv("local_data_base_test/geonames.csv", low_memory=False)

    # creates empty dataframe to append data
    df = pd.DataFrame(
        columns=['place name', 'tweet text', 'geonames id', 'geonames string'])
    i = 0
    for items in entity_relations:
        [tweet] = tweets[i]
        for row in get_database_rows(items, tweet, geonames, country_info, feature_codes):
            df = pd.concat([df, pd.DataFrame.from_records([row])])
        i += 1

    df.dropna(inplace=True)
    df = df.drop_duplicates()

    df.reset_index(drop=True, inplace=True)
    return df


def get_database_rows(items, tweet, geonames, country_info, feature_codes):
    rows = []

    place_entities = get_relations(items, "place name")

    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]
        get_geonames_instance(place_entity, geonames, rows, tweet, country_info, feature_codes)

    return rows


def get_geonames_instance(place_entity, geonames, rows, tweet, country_info, feature_codes):
    geonames_instances = geonames[geonames['name'].str.lower() == place_entity.lower()]
    if not geonames_instances.empty:
        for index, row in geonames_instances.iterrows():
            if row['country'] is not np.nan:
                mask = country_info['ISO'] == row['country']
                country = country_info[mask]
                country = country.values[0]
                country_name = country[1]
                continent = country[2]
            else:
                country_name = np.nan
                continent = np.nan

            if row['fcode'] is not np.nan and row["fclass"] is not np.nan:
                code = row['fclass'] + '.' + row['fcode']
                mask = feature_codes['Code'] == code
                fcode = feature_codes[mask]
                fcode = fcode.values[0][1]
            else:
                fcode = np.nan

            geonames_list = [row['name'], row['alternatenames'],
                             country_name, continent, fcode, row['timezone']]

            cleaned_geonames_list = [item for item in geonames_list if item is not np.nan]

            rows.append(
                {'place name': place_entity, 'tweet text': tweet,
                 "geonames id": row['geonameid'], 'geonames string': ', '.join(cleaned_geonames_list)})


def get_relations(list_of_lists, target):
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
    return relations


data = read_data()
data.to_csv('quake_text_prepped_data_base_checking.csv', index=False)
