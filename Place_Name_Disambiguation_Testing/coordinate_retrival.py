import time

import pandas as pd
from geopy import GeoNames
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


def get_geonames_instance(place_entity, geolocator):
    geonames_instance_list = []
    geonames_instances = geolocator.geocode(place_entity, exactly_one=False, timeout=None)
    if geonames_instances is not None:
        for instance in geonames_instances:
            if instance.address.split(',')[0].lower() == place_entity.lower():
                geonames_instance_list.append(
                    {"Location": instance.raw.get('toponymName'), "Latitude": instance.raw.get('lat'),
                     "Longitude": instance.raw.get('lng'), "Geonames ID": instance.raw.get('geonameId')})

    return geonames_instance_list


def get_ranks(data):
    sorted_lst = []
    for index, row in data.iterrows():
        if row['Instances']:
            for instance in row["Instances"]:
                instance['Distance'] = calculate_distance(row['text_latitude'], row['text_longitude'],
                                                          instance.get('Latitude'),
                                                          instance.get('Longitude'))

            # print(row['Instances'])
            sorted_lst = sorted(row['Instances'], key=lambda x: x['Distance'])

        min_lists = [first_min, second_min, third_min]
        for idx, min_list in enumerate(min_lists):
            if len(sorted_lst) > idx:
                min_list.append(sorted_lst[idx])
            else:
                min_list.append({})


def run():
    count = 0
    data = pd.read_csv(path, low_memory=False)
    geolocator = GeoNames(username='QuakeText')
    geolocator_2 = GeoNames(username='lp776')
    geolocator_3 = GeoNames(username='20004521_lp')
    geolocator_4 = GeoNames(username='l_joy')
    geolocator_5 = GeoNames(username='temp_1')
    geolocator_6 = GeoNames(username='temp_222')
    geolocator_7 = GeoNames(username='temp_3')
    geolocator_8 = GeoNames(username='temp_4')
    geolocator_9 = GeoNames(username='temp_5')

    for index, row in data.iterrows():
        if count <= 975:
            instances.append(get_geonames_instance(row[location], geolocator))
            count += 1
        elif 975 < count <= 1950:
            instances.append(get_geonames_instance(row[location], geolocator_2))
            count += 1
        elif 1950 < count <= 2925:
            instances.append(get_geonames_instance(row[location], geolocator_3))
            count += 1
        elif 2925 < count <= 3900:
            instances.append(get_geonames_instance(row[location], geolocator_4))
            count += 1
        elif 3900 < count <= 4875:
            instances.append(get_geonames_instance(row[location], geolocator_5))
            count += 1
        elif 4875 < count <= 5850:
            instances.append(get_geonames_instance(row[location], geolocator_6))
            count += 1
        elif 5850 < count <= 6825:
            instances.append(get_geonames_instance(row[location], geolocator_7))
            count += 1
        elif 6825 < count <= 7800:
            instances.append(get_geonames_instance(row[location], geolocator_8))
            count += 1
        elif 7800 < count <= 8775:
            instances.append(get_geonames_instance(row[location], geolocator_9))
            count += 1
        else:
            time.sleep(4500)
            count = 0
        print(count)

    data['Instances'] = instances
    get_ranks(data)

    data['First Minimum'] = first_min
    data['Second Minimum'] = second_min
    data['Third Minimum'] = third_min
    data = data.drop(columns='Instances')
    data.reset_index(drop=True, inplace=True)
    data.to_csv("nerDataCleanedWithDistanceCalc.csv", index=False)


run()
