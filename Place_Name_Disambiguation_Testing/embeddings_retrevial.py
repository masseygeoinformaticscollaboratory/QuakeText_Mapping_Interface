import sys
from sklearn.manifold import TSNE
import openai
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

openai.api_key = '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'


def get_openai_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def calculate_cosine_similarity(embeddings):
    return cosine_similarity(embeddings, embeddings)


model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


path = './Cleaned_Data_Ready_For_Embeddings/CleanedNERData_Bio.csv'
data = pd.read_csv(path, low_memory=False)
input_string_list = data['text'].values.tolist()

result_inputs = []
[result_inputs.append(x) for x in input_string_list if x not in result_inputs]


open_ai_embeddings = [get_openai_embedding(x) for x in result_inputs]
# bert_embeddings = [get_bert_embedding(x) for x in place_list]
# bert_cos_sim = calculate_cosine_similarity(bert_embeddings)
openai_cos_sim = calculate_cosine_similarity(open_ai_embeddings)

