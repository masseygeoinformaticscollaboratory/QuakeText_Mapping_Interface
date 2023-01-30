from collections import defaultdict

import geocoder
import pandas as pd
import geopandas as gpd
import numpy as np


# Prepares the data to go into PostGreSQL PostGIS database
def clean_df(data: pd.DataFrame) -> gpd.GeoDataFrame:
    data = data[['label', 'instance', 'tweetText', 'tweetId']].copy()

    get_coordinates(data)
    data.sort_values(by=['tweetId'])
    data = data.reset_index(drop=True)
    return create_gdf(data)

def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan
    coordinates = {}

    for index, row in data.iterrows():
        if row['label'] == 'place name':
            g = geocoder.geonames(row['instance'], key='QuakeText')
            coordinates[row['tweetId']] = [g.lat, g.lng]

    for index, row in data.iterrows():
        for i in coordinates:
            if row['tweetId'] == i:
                data.loc[[index], 'latitude'] = coordinates[i][0]
                data.loc[[index], 'longitude'] = coordinates[i][1]

# Creates GeoDataframe with relevant information
def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326', geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf
