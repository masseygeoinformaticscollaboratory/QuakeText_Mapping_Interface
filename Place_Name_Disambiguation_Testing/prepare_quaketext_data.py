import pandas as pd
from pathlib import Path


def read_data():
    print("Reading files...")
    path = '../dataFiles'
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
    df = df.drop_duplicates()

    df.dropna(inplace=True)
    print(df)
    return df


def get_database_rows(items, tweet):
    rows = []

    place_entities = get_relations(items, "place name")

    for place in place_entities:
        place_entity = tweet[place[0]:place[1]]
        rows.append({'place name': place_entity, 'tweet text': tweet})
    return rows


def get_relations(list_of_lists, target):
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
    return relations
