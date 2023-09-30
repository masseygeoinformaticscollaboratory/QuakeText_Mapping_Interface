import ast

import pandas as pd
import statistics
from geopy.distance import geodesic as gd

path = "../CompletedBertEmbeddings/LGLBertCompleted.csv"


def calculate_distance(bert_lat, bert_lng, coord_lat, coord_lng):
    bert_coords = (bert_lat, bert_lng)
    coord_cords = (coord_lat, coord_lng)
    return gd(bert_coords, coord_cords).km


def condition(x):
    return x <= 161


def main():
    data = pd.read_csv(path, low_memory=False)

    distance_error = []

    for index, row in data.iterrows():
        '''
        first_minimum = row['First Minimum']
        first_minimum = ast.literal_eval(first_minimum)
        coord_lat = first_minimum['Latitude']
        coord_lng = first_minimum['Longitude']
        '''
        coord_lat = row['lat']
        coord_lng = row['lon']
        bert_lat = row['geonames_lat_bert']
        bert_lng = row['geonames_lon_bert']

        distance_error.append(calculate_distance(bert_lat, bert_lng, coord_lat, coord_lng))

    average_error = sum(distance_error) / len(distance_error)
    median_error = statistics.median(distance_error)
    percent_161 = ((sum(condition(x) for x in distance_error)) / len(distance_error)) * 100

    print(f"Average Distance Error: {average_error}")
    print(f"Median Error: {median_error}")
    print(f"Percentage within 161km: {percent_161}")


main()
