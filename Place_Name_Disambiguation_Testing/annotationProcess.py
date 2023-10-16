import numpy as np
import pandas as pd
from sqlalchemy import text


def combine_data():
    path = '../../CompletedEmbeddings/QuakeText-071023-CompleteEmbeddings.csv'
    quakeCore = pd.read_csv(path, low_memory=False)
    dataset_1 = pd.read_csv("GeorgiaFullSet.csv", low_memory=False)
    dataset_1['True/False'] = dataset_1['True/False'].fillna(0)
    dataset_2 = pd.read_csv("SophieFullSet.csv", low_memory=False)
    dataset_2 = dataset_2.drop('Unnamed: 5', axis=1)
    dataset_2['True/False'] = dataset_2['True/False'].fillna(0)
    combined_data = pd.concat([dataset_1, dataset_2], ignore_index=True)
    combined_data = combined_data[combined_data['True/False'] != 0]
    combined_data.reset_index(drop=True, inplace=True)
    combined_data["correct_instance"] = np.nan
    for i, quake_row in quakeCore.iterrows():
        for j, data_row in combined_data.iterrows():
            if (data_row["tweet text"] == quake_row["tweet text"]) and (
                    data_row["place name"] == quake_row["place name"]):
                quakeCore.at[i, "correct_instance"] = data_row["geonames id"]
    quakeCore.dropna(subset=["correct_instance"], inplace=True)
    quakeCore = quakeCore.astype({'correct_instance': 'int'})
    quakeCore.reset_index(drop=True, inplace=True)
    quakeCore.to_csv('QuakeText-071023-CompleteEmbeddings.csv', index=False)


def get_coordinates(conn_engine):
    path = 'CompletedEmbeddings/QuakeText-071023-CompleteEmbeddings.csv'
    data = pd.read_csv(path, low_memory=False)
    data["correct_instance_lat"] = np.nan
    data["correct_instance_lon"] = np.nan
    count = 1

    for index, row in data.iterrows():
        print(f'Processing Row {count}: {row["tweet text"]}')
        count += 1
        query = text(
            f"SELECT geonameid, latitude, longitude FROM geoname WHERE geonameid = {row['correct_instance']}")
        result = conn_engine.execute(query).fetchone()
        if result:
            geonameid, latitude, longitude = result
            data.at[index, "correct_instance_lat"] = latitude
            data.at[index, "correct_instance_lon"] = latitude

    data.dropna(subset=["correct_instance_lat"], inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.to_csv('QuakeText-071023-CompleteEmbeddings.csv', index=False)
