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

# place_list = ["Auckland, New Zealand", "Albany, Auckland, New Zealand", "Albany, New York", "Albany, Australia", "Wellington, New Zealand", "Paris, France", "Giza, Egypt", "Cairo, Egypt", "Rome, Italy", "Wainui, Auckland", "Wainui, Auckland, NZ", "Wainui, Canterbury", "Auckland", "Albany", "Wellington", "Paris", "Giza", "Cairo", "Rome", "Wainui", "Glasseye Creek Ecological Area", "Ōtānerua"]
place_list = ["Wainui, Waitoki",
              "Wainui, horses",
              "Wainui, farmland",
              "Wainui, farmland, horses, school",
              "Wainui, Waitoki, farmland, horses, school",

              "Wainui, Gisbourne, New Zealand, populated place",
              "Wainui, Canterbury, New Zealand, locality",
              "Wainui, Auckland, New Zealand, locality",
              "Wainui, Bay of Plenty, New Zealand, locality",
              "Wainui, Northland, New Zealand, locality",
              "Wainui, Otago, New Zealand, farmstead",
              "Wainui, Queensland, Australia, populated place",
              "Wainui, New South Wales, Australia, populated place",
              "Wainui, Wellington, New Zealand, mountain",
              "Wainui, Canterbury, New Zealand, populated place",
              "Wainui, Wellington, New Zealand, hill",
              "Wainui, New Zealand, stream",
              "Wainui, Victoria, Australia, homestead",
              "Wainui, Gisbourne, New Zealand, farmstead",
              "Wainui, Hawke’s Bay, New Zealand, populated place"]

openai.api_key = '#open ai key here#'


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


open_ai_embeddings = [get_openai_embedding(x) for x in place_list]
bert_embeddings = [get_bert_embedding(x) for x in place_list]
bert_cos_sim = calculate_cosine_similarity(bert_embeddings)
openai_cos_sim = calculate_cosine_similarity(open_ai_embeddings)
