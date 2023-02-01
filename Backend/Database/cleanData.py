import geocoder
import pandas as pd
import geopandas as gpd
import numpy as np
import time


# Prepares the data to go into PostGreSQL PostGIS database
def clean_df(data: pd.DataFrame) -> gpd.GeoDataFrame:

    data = data[['label', 'instance', 'tweetText', 'tweetId']].copy()
    data = data[data.label == "place name"]

    get_coordinates(data)
    data.sort_values(by=['tweetId'])
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)

    return create_gdf(data)

def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan

    for index, row in data.iterrows():
        if row['label'] == 'place name':
            g = geocoder.geonames(row['instance'], key='QuakeText')
            if g.current_result:
                data.loc[[index], 'latitude'] = g.lat
                data.loc[[index], 'longitude'] = g.lng


# Creates GeoDataframe with relevant information
def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326', geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf
