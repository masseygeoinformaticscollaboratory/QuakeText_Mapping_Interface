import geocoder
import pandas as pd
import geopandas as gpd

def clean_df(data: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    A function to prepare the dataframe before converting to PostgresDB
    """
    data = data[['label', 'instance', 'tweetText', 'tweetId']].copy()
    place_name_df = data[data.label == 'place name']
    new_df = data[data['label'].str.contains("place name") == False]

    place_name_df = get_coords(place_name_df)

    result = pd.concat([place_name_df, new_df])
    result.sort_values(by=['tweetId'])
    result = result.reset_index(drop=True)
    gdf = create_gdf(result)
    return gdf

def get_coords(place_name_df):
    lat_list = []
    lng_list = []
    place_name_df = place_name_df.reset_index(drop=True)
    for index, row in place_name_df.iterrows():
        g = geocoder.geonames(row['instance'], key='QuakeText')
        lat_list.append(g.lat)
        lng_list.append(g.lng)
    place_name_df['latitude'] = lat_list
    place_name_df['longitude'] = lng_list
    return place_name_df

def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326',geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf
