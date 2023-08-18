import pandas as pd
from geopy import GeoNames
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import openai

openai.api_key = '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'


def get_openai_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def calculate_cosine_similarity(embeddings_1, embeddings_2):
    return cosine_similarity(embeddings_1, embeddings_2)


model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def get_geonames_instance(place_entity):
    geolocator = GeoNames(username='QuakeText')
    geonames_string_list = []
    geonames_instances = geolocator.geocode(place_entity, exactly_one=False, timeout=None)
    if geonames_instances is not None:
        for instance in geonames_instances:
            if instance.address.split(',')[0].lower() == place_entity.lower():
                geonames_list = [instance.raw.get('toponymName'), instance.raw.get('countryName'),
                                 instance.raw.get(
                                     'countryCode'), instance.raw.get('fcodeName'),
                                 instance.raw.get('fcodeName')]
                cleaned_geonames_list = [item for item in geonames_list if item is not None]

                geonames_string_list.append(', '.join(cleaned_geonames_list))
    return geonames_string_list



def run():
    path = './Cleaned_Data_Ready_For_Embeddings/CleanedNERData_Bio.csv'
    data = pd.read_csv(path, low_memory=False)
    result_inputs = []
    input_string_list = data['text'].values.tolist()

    result_inputs = [
        "USGS reports a M4.9 #earthquake 104km NNE of Awaran, Pakistan on 9/27/13 @ 18:08:41 UTC http://t.co/CRqbclzQyQ #quake"]
    geonames_instances = get_geonames_instance('Awaran')

    print(geonames_instances)

    # [result_inputs.append(x) for x in input_string_list if x not in result_inputs]
    # input_string_embeddings = [get_openai_embedding(x) for x in result_inputs]
    # openai_cos_sim = calculate_cosine_similarity(open_ai_embeddings)

    input_string_embeddings_bert = [get_bert_embedding(x) for x in result_inputs]
    geo_names_embeddings_bert = [get_bert_embedding(x) for x in geonames_instances]
    #print(input_string_embeddings_bert)
    bert_cos_sim = calculate_cosine_similarity(input_string_embeddings_bert, geo_names_embeddings_bert)
    print(bert_cos_sim)


run()
