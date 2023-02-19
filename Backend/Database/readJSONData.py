import geocoder
import geopandas as gpd
import numpy as np
import pandas as pd


def get_json_data():
    data = pd.read_json('../jsonData/pred1.json', lines=True)
    relations = data.get("relations")
    sentences = data.get("sentences")
    df = pd.DataFrame(
        columns=['place name', 'type of impact', 'impact place relation', 'tweet text', 'impact category'])
    i = 0
    for impacts in relations:
        [impact_list] = impacts
        [sentence] = sentences[i]
        for impact in impact_list:
            df = pd.concat([df, pd.DataFrame.from_records([get_impact_relations(impact, sentence)])])
        i += 1
    df['type of impact'] = df['type of impact'].apply(str.title)
    df = get_impact_category(df.reset_index(drop=True))
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


def get_impact_category(data):
    damage = ['Damage', 'Damages', 'Damaged', 'Collapse', 'Collapsed', 'Down', 'Destroyed', 'Destroy', 'Destroys']
    death = ['Dead', 'Killed', 'Kill', 'Kills', 'Die', 'Dies', 'Died', 'Loss', 'Loss Of Life', 'Death Toll', 'Claims',
             'Claim', 'Death', 'Deaths', 'Deads', 'Daed']
    fire = ['Fire', 'Fires', 'Flames', 'Flame', 'Blaze', 'Smoke']
    flood = ['Flood', 'Floods', 'Wash Away', 'Sweep Away', 'Submerge', 'Flood Hits']
    injury = ['Injured', 'Injury', 'Injuries', 'Injures', 'Hurt', 'Hurts']
    missing = ['Missing', 'Missing Person', 'Missing People']
    terrorism = ['Bombing', 'Bomb']
    trapped = ['Trap', 'Traps', 'Marooned', 'Maroon', 'Maroons', 'Stranded', 'Strands', 'Strand']

    for index, row in data.iterrows():
        impact = row["type of impact"]

        match impact:
            case impact if impact in damage:
                data.loc[[index], 'impact category'] = 'Damage'
            case impact if impact in death:
                data.loc[[index], 'impact category'] = 'Death'
            case impact if impact in fire:
                data.loc[[index], 'impact category'] = 'Fire'
            case impact if impact in flood:
                data.loc[[index], 'impact category'] = 'Flood'
            case impact if impact in injury:
                data.loc[[index], 'impact category'] = 'Injury'
            case impact if impact in missing:
                data.loc[[index], 'impact category'] = 'Missing'
            case impact if impact in terrorism:
                data.loc[[index], 'impact category'] = 'Terrorism'
            case impact if impact in trapped:
                data.loc[[index], 'impact category'] = 'Trapped'
            case _:
                data.loc[[index], 'impact category'] = 'Other'

    return data


def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan

    for index, row in data.iterrows():
        impact = row["type of impact"]

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
