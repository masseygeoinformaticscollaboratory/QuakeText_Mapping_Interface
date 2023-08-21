import time
import numpy as np
import pandas as pd
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
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def calculate_cosine_similarity(embeddings_1, embeddings_2):
    return cosine_similarity(embeddings_1, embeddings_2)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def get_geonames_instance(place_entity, geonames, country_info, feature_codes):
    geonames_instances_lst = []
    geonames_instances = geonames[geonames['name'].str.lower() == place_entity.lower()]
    if not geonames_instances.empty:
        for index, row in geonames_instances.iterrows():
            if row['country'] is not np.nan:
                mask = country_info['ISO'] == row['country']
                country = country_info[mask]
                country = country.values[0]
                country_name = country[1]
                continent = country[2]
            else:
                country_name = np.nan
                continent = np.nan

            if row['fcode'] is not np.nan and row["fclass"] is not np.nan:
                code = row['fclass'] + '.' + row['fcode']
                mask = feature_codes['Code'] == code
                fcode = feature_codes[mask]
                fcode = fcode.values[0][1]
            else:
                fcode = np.nan

            geonames_list = [row['name'], row['alternatenames'],
                             country_name, continent, fcode, row['timezone']]

            cleaned_geonames_list = [item for item in geonames_list if item is not np.nan]

            geonames_instances_lst.append({"Geonames String": ', '.join(cleaned_geonames_list),
                                           "Geonames ID": row['geonameid'],
                                           "Geonames Latitude": row['latitude'],
                                           "Geonames Longitude": row['longitude']})

    return geonames_instances_lst


def run():
    start = time.time()

    # Initialise data
    path = 'Cleaned_Data_Ready_For_Embeddings/quake_text_prepped_data.csv'
    text = 'tweet text'
    location = 'place name'
    data = pd.read_csv(path, low_memory=False)
    country_info = pd.read_csv("local_data_base_test/countryInfo.csv", low_memory=False)
    country_info = country_info[['ISO', 'Country', 'Continent']]
    feature_codes = pd.read_csv("local_data_base_test/featureCodes.csv", low_memory=False)
    geonames = pd.read_csv("local_data_base_test/geonames.csv", low_memory=False)
    data["open ai"] = np.nan
    data["geonames_lat_openai"] = np.nan
    data["geonames_lon_openai"] = np.nan
    data["geonames_id_openai"] = np.nan

    data["bert"] = np.nan
    data["geonames_lat_bert"] = np.nan
    data["geonames_lon_bert"] = np.nan
    data["geonames_id_bert"] = np.nan

    for index, row in data.iterrows():
        geonames_instances = get_geonames_instance(row[location], geonames, country_info, feature_codes)
        geonames_strings = []
        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            # For each row in the dataset retrieve the embeddings for the text and calculate the cos sim

            input_string_embedding_openai = [get_openai_embedding(x) for x in [row[text]]]
            geo_names_embeddings_openai = [get_openai_embedding(x) for x in geonames_strings]
            openai_cos_sim = calculate_cosine_similarity(input_string_embedding_openai, geo_names_embeddings_openai)

            # Find the max cosine distance assuming this is < 1
            max_sim_openai = np.max(openai_cos_sim)

            data.at[index, "open ai"] = max_sim_openai
            data.at[index, "geonames_lat_openai"] = geonames_instances[
                np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_openai"] = geonames_instances[
                np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Longitude')
            data.at[index, "geonames_id_openai"] = geonames_instances[
                np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames ID')

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

    data = data.dropna(subset=["bert"])
    data = data.astype({'geonames_id_bert': 'int'})
    data = data.astype({'geonames_id_openai': 'int'})

    data.to_csv('QuakeTextCompletedEmbeddings.csv', index=False)
    end = time.time()
    print(f"Total time taken: {end - start}")


run()
