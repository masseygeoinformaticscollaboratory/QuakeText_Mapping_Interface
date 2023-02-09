import geocoder
import geopandas as gpd
import numpy as np
import pandas as pd


def get_json_data():
    data = pd.read_json('../jsonData/2JsonData.json', lines=True)
    ner = data.get("ner")
    sentences = data.get("sentences")
    return clean_data(ner, sentences)


def clean_data(ner, sentences):
    df = pd.DataFrame(
        columns=['place name', 'location modifier', 'severity or quantity', 'item affected', 'type of impact',
                 'tweet text'])
    i = 0
    for row in ner:
        place_names = []
        location_mods = []
        affected_items = []
        impact_type = []
        severity_quantity = []
        for column in row:
            for item in column:
                start = item[0]
                end = item[1]
                match item[2]:
                    case "place name":
                        place_names.extend(sentences.get(i)[0][start:end + 1])
                    case "location modifier":
                        location_mods.extend(sentences.get(i)[0][start:end + 1])
                    case "severity or quantity":
                        severity_quantity.extend(sentences.get(i)[0][start:end + 1])
                    case "item affected":
                        affected_items.extend(sentences.get(i)[0][start:end + 1])
                    case "type of impact":
                        impact_type.extend(sentences.get(i)[0][start:end + 1])

        df = pd.concat([df, pd.DataFrame.from_records([{
            'place name': ','.join(place_names),
            'location modifier': ','.join(location_mods),
            'severity or quantity': ','.join(severity_quantity),
            'item affected': ','.join(affected_items),
            'type of impact': ','.join(impact_type),
            'tweet text': ' '.join(sentences.get(i)[0]),
        }])])
        i += 1
    df = df.reset_index(drop=True)

    get_coordinates(df)
    return create_gdf(df)


def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan

    for index, row in data.iterrows():
        g = geocoder.geonames(row['place name'], key='QuakeText')
        if g.current_result:
            data.loc[[index], 'latitude'] = g.lat
            data.loc[[index], 'longitude'] = g.lng


def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326', geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf


