import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from sqlalchemy import text
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import concurrent.futures

# Initialise data
path = 'test.csv'
tweet = 'text'
location = 'location'

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def calculate_cosine_similarity(embeddings_1, embeddings_2):
    return cosine_similarity(embeddings_1, embeddings_2)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def get_geonames_instance(place_entity, conn_engine):
    geonames_instances_lst = []
    place_entity_escaped = place_entity.replace("'", "")
    query = text(
        f"SELECT * FROM geoname WHERE name ILIKE '% {place_entity_escaped} %' OR name ILIKE '{place_entity_escaped} %' OR name ILIKE '% {place_entity_escaped}' OR name ILIKE '{place_entity_escaped}'")

    matching_rows = conn_engine.execute(query)

    geonames_instances = pd.DataFrame(matching_rows.fetchall(), columns=matching_rows.keys())

    if not geonames_instances.empty:
        num_threads = 16  # Adjust this based on your requirements
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit the tasks to the executor and retrieve the results
            geonames_instances_lst = list(
                executor.map(lambda x: process_geonames_row(conn_engine, x[1]), geonames_instances.iterrows()))

    return geonames_instances_lst


def process_geonames_row(conn_engine, row):
    country_name = None
    continent = None
    if row['country'] is not None:
        query = text(f"SELECT * FROM countryinfo WHERE ISO = '{row['country']}'")
        country = conn_engine.execute(query).fetchone()

        if country is not None:
            country_name = country[1]
            continent = country[2]
    fcode = None
    if row['fcode'] is not None and row["fclass"] is not None:
        code = row['fclass'] + '.' + row['fcode']
        query = text(f"SELECT * FROM featurecodes WHERE code = '{code}'")
        features = conn_engine.execute(query).fetchone()
        if features is not None:
            fcode = features[1]
    geonames_list = [row['name'], row['alternatenames'],
                     country_name, continent, fcode]
    cleaned_geonames_list = [item for item in geonames_list if item is not None]
    return {"Geonames String": ', '.join(cleaned_geonames_list),
            "Geonames ID": row['geonameid'],
            "Geonames Latitude": row['latitude'],
            "Geonames Longitude": row['longitude']}


def run(conn_engine):
    print("Beginning process")
    start = time.time()

    data = pd.read_csv(path, low_memory=False)

    data["bert"] = np.nan
    data["geonames_lat_bert"] = np.nan
    data["geonames_lon_bert"] = np.nan
    data["geonames_id_bert"] = np.nan

    for index, row in data.iterrows():
        geonames_instances = get_geonames_instance(row[location], conn_engine)
        geonames_strings = []
        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            input_string_embeddings_bert = [get_bert_embedding(x) for x in [row[tweet]]]

            num_threads = 16

            # Create a ThreadPoolExecutor with the specified number of threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit the tasks to the executor and retrieve the results
                results = list(executor.map(get_bert_embedding, geonames_strings))

            geo_names_embeddings_bert = results

            bert_cos_sim = calculate_cosine_similarity(input_string_embeddings_bert, geo_names_embeddings_bert)
            max_sim_bert = np.max(bert_cos_sim)

            data.at[index, "bert"] = max_sim_bert
            data.at[index, "geonames_lat_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Longitude')
            data.at[index, "geonames_id_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames ID')

    data = data.dropna(subset=["bert"])
    data = data.astype({'geonames_id_bert': 'int'})

    data.to_csv('TestMultiBert.csv', index=False)

    end = time.time()
    print(f"Total time taken: {end - start}")
