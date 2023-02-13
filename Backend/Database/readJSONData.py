import geocoder
import geopandas as gpd
import numpy as np
import pandas as pd


def get_json_data():
    data = pd.read_json('../jsonData/strangePlace.json', lines=True)
    relations = data.get("relations")
    sentences = data.get("sentences")
    df = pd.DataFrame(
        columns=['place name', 'type of impact', 'impact place relation', 'tweet text'])
    i = 0
    for impacts in relations:
        [impact_list] = impacts
        [sentence] = sentences[i]
        for impact in impact_list:
            df = pd.concat([df, pd.DataFrame.from_records([get_impact_relations(impact, sentence)])])
        i += 1

    df = get_coordinates(df.reset_index(drop=True))
    df.dropna(inplace=True)

    return create_gdf(df)


def get_impact_relations(impact_list, sentence):
    if impact_list[0] == impact_list[1]:
        impact = ' '.join(sentence[impact_list[0]:impact_list[1] + 1])
    else:
        impact = ' '.join(sentence[impact_list[0]:impact_list[1]])

    if impact_list[2] == impact_list[3]:
        place = ' '.join(sentence[impact_list[2]:impact_list[3] + 1])
    else:
        place = ' '.join(sentence[impact_list[2]:impact_list[3]])
    return {
        'place name': place,
        'type of impact': impact,
        'impact place relation': impact + " " + place,
        'tweet text': ' '.join(sentence),
    }


def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan

    for index, row in data.iterrows():
        g = geocoder.geonames(row['place name'], key='QuakeText')
        if g.current_result:
            data.loc[[index], 'latitude'] = g.lat
            data.loc[[index], 'longitude'] = g.lng
        else:
            print("Unable to find:" + row['place name'] + ' in geonames')

    return data


def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326', geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf
