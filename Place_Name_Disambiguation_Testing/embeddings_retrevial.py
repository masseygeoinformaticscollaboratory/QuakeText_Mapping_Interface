import time
import numpy as np
import pandas as pd
from sqlalchemy import text
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import openai
import config

openai.api_key = config.api_key

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def get_openai_embedding(text, model="text-embedding-ada-002"):
    try:
        text = text.replace("\n", " ")
        return openai.Embedding.create(input=[text], model=model, timeout=2000)['data'][0]['embedding']
    except openai.error.Timeout as e:
        print(f"Request timed out for input text: {text} ", e)
        return None


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
    query = text(f"SELECT * FROM geoname WHERE name ILIKE '% {place_entity_escaped} %'")

    matching_rows = conn_engine.execute(query)

    geonames_instances = pd.DataFrame(matching_rows.fetchall(), columns=matching_rows.keys())

    if not geonames_instances.empty:
        for index, row in geonames_instances.iterrows():
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

            geonames_instances_lst.append({"Geonames String": ', '.join(cleaned_geonames_list),
                                           "Geonames ID": row['geonameid'],
                                           "Geonames Latitude": row['latitude'],
                                           "Geonames Longitude": row['longitude']})

    return geonames_instances_lst


def run(conn_engine):
    print("Beginning process")
    start = time.time()

    # Initialise data
    path = 'NLPBertCompleted.csv'
    text = 'tweet_text'
    location = 'location'
    data = pd.read_csv(path, low_memory=False)

    data["open ai"] = np.nan
    data["geonames_lat_openai"] = np.nan
    data["geonames_lon_openai"] = np.nan
    data["geonames_id_openai"] = np.nan
    '''
    data["bert"] = np.nan
    data["geonames_lat_bert"] = np.nan
    data["geonames_lon_bert"] = np.nan
    data["geonames_id_bert"] = np.nan
    '''
    count = 1
    for index, row in data.iterrows():
        start = time.time()
        print(f"Tweet Number {count}: {row['tweet_text']}")
        count += 1

        geonames_instances = get_geonames_instance(row[location], conn_engine)
        geonames_strings = []

        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            print(f"Number of Geonames Instances: {len(geonames_instances)}")

            #OpenAI Embeddings:
            input_string_embedding_openai = []
            for x in [row[text]]:
                embedding = get_openai_embedding(x)
                if embedding is not None:
                    input_string_embedding_openai.append(embedding)

            geo_names_embeddings_openai = []
            for x in geonames_strings:
                embedding = get_openai_embedding(x)
                if embedding is not None:
                    geo_names_embeddings_openai.append(embedding)

            openai_cos_sim = calculate_cosine_similarity(input_string_embedding_openai, geo_names_embeddings_openai)
            if openai_cos_sim is not None:
                # Find the max cosine distance assuming this is < 1
                max_sim_openai = np.max(openai_cos_sim)

                data.at[index, "open ai"] = max_sim_openai
                data.at[index, "geonames_lat_openai"] = geonames_instances[
                    np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Latitude')
                data.at[index, "geonames_lon_openai"] = geonames_instances[
                    np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Longitude')
                data.at[index, "geonames_id_openai"] = geonames_instances[
                    np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames ID')
            else:
                data.at[index, "open ai"] = np.nan
                data.at[index, "geonames_lat_openai"] = np.nan
                data.at[index, "geonames_lon_openai"] = np.nan
                data.at[index, "geonames_id_openai"] = np.nan
            '''
            #Get bert embeddings and add to dataframe:
            input_string_embeddings_bert = [get_bert_embedding(x) for x in [row[text]]]
            geo_names_embeddings_bert = [get_bert_embedding(x) for x in geonames_strings]
            bert_cos_sim = calculate_cosine_similarity(input_string_embeddings_bert, geo_names_embeddings_bert)
            max_sim_bert = np.max(bert_cos_sim)

            data.at[index, "bert"] = max_sim_bert
            data.at[index, "geonames_lat_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Longitude')
            data.at[index, "geonames_id_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames ID')

            end = time.time()
            print(f"Time taken: {end - start}")
            '''
            end = time.time()
            print(f"Time taken: {end - start}")

    data = data.dropna(subset=["bert"])
    data = data.astype({'geonames_id_bert': 'int'})
    # data = data.astype({'geonames_id_openai': 'int'})

    data.to_csv('NLPEmbeddingsComplete.csv', index=False)

    end = time.time()
    print(f"Total time taken: {end - start}")
