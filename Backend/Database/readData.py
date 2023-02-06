import csv
from pathlib import Path
import geocoder
import pandas as pd
import geopandas as gpd
import numpy as np
import time


# Reads in the data and Prepares it to go into PostGreSQL PostGIS database
def read_data():
    path = '../dataFiles'
    files = Path(path).glob('*.csv')
    dfs = list()
    for f in files:
        file = open(f, "r")
        if file.readline() != 'read\n':
            data = pd.read_csv(f)
            data['file'] = f.stem
            dfs.append(data)
            line_prepender(f)
    if len(dfs) < 1:
        return pd.DataFrame(dfs)
    else:
        return clean_df(pd.concat(dfs, ignore_index=True))


def line_prepender(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('read' + '\n' + content)


def clean_df(data: pd.DataFrame) -> gpd.GeoDataFrame:
    data = data[['label', 'instance', 'tweetText', 'tweetId']].copy()
    data = data[data.label == "place name"]

    get_coordinates(data)
    data.sort_values(by=['tweetId'])
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)

    return create_gdf(data)

# Gets the coordinates from geonames and adds them to the data frame
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
