import ast

import pandas as pd
import statistics
from geopy.distance import geodesic as gd

path = "../CompletedEmbeddings/LGL512-Instructor1-CompleteEmbeddings.csv"


def calculate_distance(LLM_lat, LLM_lon, coord_lat, coord_lng):
    LLM_coords = (LLM_lat, LLM_lon)
    coord_cords = (coord_lat, coord_lng)
    return gd(LLM_coords, coord_cords).km


def condition(x):
    return x <= 161


def main():
    data = pd.read_csv(path, low_memory=False)

    distance_error = []

    for index, row in data.iterrows():
        lat = 'geonames_lat_instructor'
        lon = 'geonames_lon_instructor'

        '''
        # For BioWhere and NLP Data
        first_minimum = row['First Minimum']
        first_minimum = ast.literal_eval(first_minimum)
        coord_lat = first_minimum['Latitude']
        coord_lng = first_minimum['Longitude']
        '''

        '''
        # For QuadTred
        coord_lat = row['correct_instance_lat']
        coord_lng = row['correct_instance_lon']

        '''   
       # For LGL
        coord_lat = row['lat']
        coord_lng = row['lon']



        LLM_lat = row[lat]
        LLM_lon = row[lon]

        distance_error.append(calculate_distance(LLM_lat, LLM_lon, coord_lat, coord_lng))

    average_error = sum(distance_error) / len(distance_error)
    median_error = statistics.median(distance_error)
    percent_161 = ((sum(condition(x) for x in distance_error)) / len(distance_error)) * 100

    print(f"Average Distance Error: {average_error}")
    print(f"Median Error: {median_error}")
    print(f"Percentage within 161km: {percent_161}")


main()
