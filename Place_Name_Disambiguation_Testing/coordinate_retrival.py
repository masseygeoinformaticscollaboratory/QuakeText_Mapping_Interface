import time

import numpy as np
import pandas as pd
from geopy.distance import geodesic as gd

path = 'Cleaned_Data_Ready_For_Embeddings/CleanedNERData_Bio.csv'
location = 'location'
first_min = []
second_min = []
third_min = []
instances = []


def calculate_distance(geo_lat, geo_lon, ori_lat, ori_lon):
    geonames_coordinates = (geo_lat, geo_lon)
    original_coordinates = (ori_lat, ori_lon)
    return gd(geonames_coordinates, original_coordinates).km


def get_geonames_instance(place_entity, geonames):
    geonames_instances = geonames[geonames['name'].str.lower() == place_entity.lower()]
    geonames_instance_list = []
    if not geonames_instances.empty:
        for index, row in geonames_instances.iterrows():
            geonames_instance_list.append(
                {"Location": row['name'], "Latitude": row['latitude'],
                 "Longitude": row['longitude'], "Geonames ID": row['geonameid']})
    else:
        geonames_instance_list.append(np.nan)
    return geonames_instance_list


def get_ranks(data):
    sorted_lst = []
    for index, row in data.iterrows():
        if row['Instances']:
            for instance in row["Instances"]:
                if instance.get('Latitude') is not np.nan:
                    instance['Distance'] = calculate_distance(row['text_latitude'], row['text_longitude'],
                                                              instance.get('Latitude'),
                                                              instance.get('Longitude'))
                else:
                    instance['Distance'] = np.nan

            # print(row['Instances'])
            sorted_lst = sorted(row['Instances'], key=lambda x: x['Distance'])

        min_lists = [first_min, second_min, third_min]
        for idx, min_list in enumerate(min_lists):
            if len(sorted_lst) > idx:
                min_list.append(sorted_lst[idx])
            else:
                min_list.append({})


def run():
    start = time.time()

    geonames = pd.read_csv('local_data_base_test/geonames.csv', low_memory=False)
    start_2 = time.time()

    data = pd.read_csv(path, low_memory=False)

    for index, row in data.iterrows():
        instances.append(get_geonames_instance(row[location], geonames))

    data['Instances'] = instances

    get_ranks(data)

    data['First Minimum'] = first_min
    data['Second Minimum'] = second_min
    data['Third Minimum'] = third_min
    data = data.drop(columns='Instances')

    data = data[data['First Minimum'].apply(lambda d: 'Latitude' not in d or not pd.isna(d['Latitude']))]

    data.reset_index(drop=True, inplace=True)
    data.to_csv("nerDataCleanedWithDistanceCalc.csv", index=False)
    end = time.time()
    print(f"Total Time Taken: {end - start}")
    print(f"Time Taken without reading Geonames in: {end - start_2}")


run()
