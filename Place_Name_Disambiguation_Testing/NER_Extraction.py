import pandas as pd
from flair.nn import Classifier
from flair.data import Sentence

# load the model
tagger = Classifier.load('ner')

# predict NER tags

original_data = pd.read_csv('output.csv', low_memory=False)
new_data = pd.DataFrame(columns=['text', 'location', 'text_latitude', 'text_longitude'])
for index, row in original_data.iterrows():
    sentence = Sentence(row['text'])
    tagger.predict(sentence)
    for label in sentence.get_labels():
        if label.value == "LOC":
            new_data = pd.concat(
                [new_data, pd.DataFrame.from_records([{"text": row["text"], "location": label.data_point.text,
                                                       "text_latitude": row['Latitude'],
                                                       "text_longitude": row['Longitude']}])])
new_data.reset_index(drop=True, inplace=True)
new_data.to_csv("nerDataCleaned.csv", index=False)
