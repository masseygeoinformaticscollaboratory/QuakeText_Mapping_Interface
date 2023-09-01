import time

import pandas as pd
from sqlalchemy import text

count = 1


def read_data(conn_engine):
    print("Reading files...")
    path = 'quaketext.json'

    # files = Path(path).glob('*.json')
    dfs = list()
    # for f in files:
    current_data = pd.read_json(path)
    dfs.append(current_data)
    return clean_df(pd.concat(dfs, ignore_index=True), conn_engine)


def clean_df(data_frame: pd.DataFrame, conn_engine):
    print("Cleaning Data...")
    relations_list = data_frame.get("relations")
    tweets = data_frame.get("tweet")
    entity_list = data_frame.get("entities")
    entity_relations = entity_list + relations_list

    # creates empty dataframe to append data
    row_list = []
    df = pd.DataFrame(
        columns=['place name', 'tweet text', 'geonames id', 'geonames string'])
    i = 0
    for items in entity_relations:
        [tweet] = tweets[i]
        rows = get_database_rows(items, tweet, conn_engine)

        for row in rows:
            row_list.append(row)

        i += 1
    df = pd.DataFrame.from_records(row_list)
    df.dropna(inplace=True)
    df = df.drop_duplicates()

    df.reset_index(drop=True, inplace=True)
    return df


def get_database_rows(items, tweet, conn_engine):
    global count
    rows = []
    place_entities = get_relations(items, "place name")
    print(f"Tweet number {count}: " + tweet)
    count += 1
    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]
        print("Place name in tweet: " + place_entity)
        start = time.time()
        get_geonames_instance(place_entity, rows, tweet, conn_engine)
        end = time.time()
        print(f"Time taken for retreival: {end - start}")
    print()

    return rows


def get_geonames_instance(place_entity, rows, tweet, conn_engine):
    place_entity_escaped = place_entity.replace("'", "")
    query = text(f"SELECT * FROM geoname WHERE name ILIKE '%%{place_entity_escaped}%%'")
    matching_rows = conn_engine.execute(query)
    geonames_instances = pd.DataFrame(matching_rows.fetchall(), columns=matching_rows.keys())

    if not geonames_instances.empty:
        for index, row in geonames_instances.iterrows():
            country_name = None
            continent = None
            if row['country'] is not None:
                query = text(f"SELECT * FROM countryinfo WHERE ISO = '{row['country']}'")
                country = conn_engine.execute(query).fetchone()
                if country is not None:
                    country_name = country[1]
                    continent = country[2]

            fcode = None
            if row['fcode'] is not None and row["fclass"] is not None:
                code = row['fclass'] + '.' + row['fcode']
                query = text(f"SELECT * FROM featurecodes WHERE code = '{code}'")
                features = conn_engine.execute(query).fetchone()
                if features is not None:
                    fcode = features[1]

            geonames_list = [row['name'], row['alternatenames'],
                             country_name, continent, fcode]

            cleaned_geonames_list = [str(item) if item is not None else "" for item in geonames_list]

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
