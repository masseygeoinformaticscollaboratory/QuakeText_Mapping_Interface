import time
import numpy as np
import pandas as pd
from geopy import GeoNames
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import openai
import config

openai.api_key = config.api_key
batch_size = 100
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
geolocator = GeoNames(username='QuakeText')


def get_openai_embedding(text, model="text-embedding-ada-002"):
    time.sleep(20)
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def calculate_cosine_similarity(embeddings_1, embeddings_2):
    return cosine_similarity(embeddings_1, embeddings_2)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def get_geonames_instance(place_entity):
    geonames_instances_lst = []
    geonames_instances = geolocator.geocode(place_entity, exactly_one=False, timeout=None)
    if geonames_instances is not None:
        for instance in geonames_instances:
            if instance.address.split(',')[0].lower() == place_entity.lower():
                geonames_list = [instance.raw.get('toponymName'), instance.raw.get('countryName'),
                                 instance.raw.get(
                                     'countryCode'), instance.raw.get('fcodeName')]

                cleaned_geonames_list = [item for item in geonames_list if item is not None]

                geonames_instances_lst.append({"Geonames String": ', '.join(cleaned_geonames_list),
                                               "Geonames Latitude": instance.raw.get('lat'),
                                               "Geonames Longitude": instance.raw.get('lng')})

    return geonames_instances_lst


def run():
    start = time.time()
    path = 'test.csv'
    text = 'text'
    location = 'location'
    data = pd.read_csv(path, low_memory=False)

    data["open ai"] = np.nan
    data["geonames_lat_openai"] = np.nan
    data["geonames_lon_openai"] = np.nan
    data["bert"] = np.nan
    data["geonames_lat_bert"] = np.nan
    data["geonames_lon_bert"] = np.nan

    for index, row in data.iterrows():
        geonames_instances = get_geonames_instance(row[location])
        geonames_strings = []
        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            input_string_embedding_openai = [get_openai_embedding(x) for x in [row[text]]]
            geo_names_embeddings_openai = [get_openai_embedding(x) for x in geonames_strings]
            openai_cos_sim = calculate_cosine_similarity(input_string_embedding_openai, geo_names_embeddings_openai)

            max_sim_openai = 0

            for sim in openai_cos_sim[0]:
                if max_sim_openai < sim:
                    max_sim_openai = sim

            data.at[index, "open ai"] = max_sim_openai
            data.at[index, "geonames_lat_openai"] = geonames_instances[
                np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_openai"] = geonames_instances[
                np.argwhere(openai_cos_sim[0] == max_sim_openai)[0][0]].get('Geonames Longitude')

            input_string_embeddings_bert = [get_bert_embedding(x) for x in [row[text]]]
            geo_names_embeddings_bert = [get_bert_embedding(x) for x in geonames_strings]
            bert_cos_sim = calculate_cosine_similarity(input_string_embeddings_bert, geo_names_embeddings_bert)

            max_sim_bert = 0
            for sim in bert_cos_sim[0]:
                if max_sim_bert < sim:
                    max_sim_bert = sim

            data.at[index, "bert"] = max_sim_bert
            data.at[index, "geonames_lat_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_bert"] = geonames_instances[
                np.argwhere(bert_cos_sim[0] == max_sim_bert)[0][0]].get('Geonames Longitude')

    data.to_csv('testComp.csv', index=False)
    end = time.time()
    print(end - start)


run()


