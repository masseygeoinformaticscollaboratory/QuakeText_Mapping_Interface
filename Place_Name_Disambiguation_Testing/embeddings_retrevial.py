import time
import numpy as np
import pandas as pd
from sqlalchemy import text
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import openai
import config
from InstructorEmbedding import INSTRUCTOR

openai.api_key = config.api_key

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)
instructor_model = INSTRUCTOR('hkunlp/instructor-large')


def get_openai_embedding(text):
    model="text-embedding-ada-002"
    for i in range(0, 5, 1):
        try:
            text = text.replace("\n", " ")
            embedding = openai.Embedding.create(input=[text], model=model, timeout=1000)['data'][0]['embedding']
            return embedding
        except Exception as e:
            time.sleep(1000)
            print(f"ERROR OCCURRED: {text} ", e)

    return None


def get_instructor_embedding(sentence):
    instruction = 'Represent the sentence for retrieving location'
    return instructor_model.encode([[instruction, sentence]])


def cosine_similarity_instructor(single_embedding, list_of_embeddings):
    similarities = cosine_similarity(single_embedding, list_of_embeddings)
    return similarities.flatten()


def calculate_cosine_similarity(embeddings_1, embeddings_2):
    return cosine_similarity(embeddings_1, embeddings_2)


def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def get_geonames_instance(place_entity, conn_engine):
    geonames_instances_lst = []
    place_entity_escaped = place_entity.replace("'", "")
    query = text(
        f"SELECT * FROM geoname WHERE name ILIKE '% {place_entity_escaped} %' OR name ILIKE '{place_entity_escaped} %' OR name ILIKE '% {place_entity_escaped}' OR name ILIKE '{place_entity_escaped}'")

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


def run_instuctor(conn_engine):
    print("Beginning process")
    start = time.time()

    # Initialise data
    path = 'CompletedEmbeddings/LGL512-Instructor1-CompleteEmbeddings.csv'
    tweet = 'text'
    location = 'location'
    data = pd.read_csv(path, low_memory=False)

    data["instructor_3"] = np.nan
    data["geonames_lat_instructor_3"] = np.nan
    data["geonames_lon_instructor_3"] = np.nan
    data["geonames_id_instructor_3"] = np.nan
    count = 1
    data = pd.read_csv(path, low_memory=False)

    for index, row in data.iterrows():
        start = time.time()
        print(f"Tweet Number {count}: {row[tweet]}")
        count += 1

        geonames_instances = get_geonames_instance(row[location], conn_engine)
        geonames_strings = []

        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:

            print(f"Number of Geonames Instances: {len(geonames_instances)}")

            # instruction_text = f'Represent the disaster tweet for retrieving {row[location]} location:'
            # instruction_text = f'Represent the geographic location description for retrieving {row[location]} location:'
            instruction_text = f'Represent the news article for retrieving {row[location]} location:'
            #instruction_text = f'Represent the news article for retrieving location:'
            # instruction_text = "Represent the sentence for retrieving geonames location"

            instruction_geonames = f'Represent the geographic location description for retrieving {row[location]} location:'
            # instruction_geonames = f'Represent the geographic location description for retrieving location:'
            # instruction_geonames = "Represent the sentence for retrieving geonames location"

            prep_geonames = []
            prep_tweet = [[instruction_text, row[tweet]]]

            for x in geonames_strings:
                prep_geonames.append([instruction_geonames, x])

            tweet_embeddings = instructor_model.encode(prep_tweet)
            geonames_embeddings = instructor_model.encode(prep_geonames)

            instructor_cos_sim = calculate_cosine_similarity(tweet_embeddings,
                                                             geonames_embeddings)

            max_sim_instructor = np.max(instructor_cos_sim)

            data.at[index, "instructor_3"] = max_sim_instructor
            data.at[index, "geonames_lat_instructor_3"] = geonames_instances[
                np.argwhere(instructor_cos_sim[0] == max_sim_instructor)[0][0]].get('Geonames Latitude')
            data.at[index, "geonames_lon_instructor_3"] = geonames_instances[
                np.argwhere(instructor_cos_sim[0] == max_sim_instructor)[0][0]].get('Geonames Longitude')
            data.at[index, "geonames_id_instructor_3"] = geonames_instances[
                np.argwhere(instructor_cos_sim[0] == max_sim_instructor)[0][0]].get('Geonames ID')

            end = time.time()
            print(f"Time taken: {end - start}")

    data = data.dropna(subset=["instructor_3"])
    data = data.astype({'geonames_id_instructor_3': 'int'})

    data.to_csv('LGL512-Instructor3-CompleteEmbeddings.csv', index=False)

    end = time.time()
    print(f"Total time taken: {end - start}")


def run_open_ai_embeddings(conn_engine):
    print("Beginning process")
    start = time.time()

    # Initialise data
    path = 'CompletedEmbeddings/QuadTred-071023-CompleteEmbeddings.csv'
    tweet = 'tweet text'
    location = 'place name'
    data = pd.read_csv(path, low_memory=False)

    data["open ai"] = np.nan
    data["geonames_lat_openai"] = np.nan
    data["geonames_lon_openai"] = np.nan
    data["geonames_id_openai"] = np.nan
    count = 1
    for index, row in data.iterrows():
        start = time.time()
        print(f"Tweet Number {count}: {row[tweet]}")
        count += 1

        geonames_instances = get_geonames_instance(row[location], conn_engine)
        geonames_strings = []

        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            print(f"Number of Geonames Instances: {len(geonames_instances)}")

            # OpenAI Embeddings:
            input_string_embedding_openai = []

            for x in [row[tweet]]:
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

            end = time.time()
            print(f"Time taken: {end - start}")

    data = data.dropna(subset=["bert"])
    data = data.astype({'geonames_id_openai': 'int'})

    data.to_csv('QuadTred-221023-CompletedEmbeddings.csv', index=False)

    end = time.time()
    print(f"Total time taken: {end - start}")


def run_bert_embeddings(conn_engine):
    print("Beginning process")
    start = time.time()

    # Initialise data
    path = 'LGLProcessed512.csv'
    tweet = 'text'
    location = 'location'
    data = pd.read_csv(path, low_memory=False)

    data["bert"] = np.nan
    data["geonames_lat_bert"] = np.nan
    data["geonames_lon_bert"] = np.nan
    data["geonames_id_bert"] = np.nan

    count = 1
    for index, row in data.iterrows():
        start = time.time()
        print(f"Tweet Number {count}: {row[tweet]}")
        count += 1

        geonames_instances = get_geonames_instance(row[location], conn_engine)
        geonames_strings = []

        for item in geonames_instances:
            geonames_strings.append(item.get("Geonames String"))
        if len(geonames_instances) > 0:
            print(f"Number of Geonames Instances: {len(geonames_instances)}")

            # Get bert embeddings and add to dataframe:
            input_string_embeddings_bert = [get_bert_embedding(x) for x in [row[tweet]]]
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

    data = data.dropna(subset=["bert"])
    data = data.astype({'geonames_id_bert': 'int'})

    data.to_csv('LGLBertCompleted512.csv', index=False)

    end = time.time()
    print(f"Total time taken: {end - start}")
