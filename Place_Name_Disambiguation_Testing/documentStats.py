import pandas as pd
import statistics
from geopy.distance import geodesic as gd
from nltk import word_tokenize

path = "CompletedEmbeddings/QuadTred-180923-CompletedEmbeddings.csv"
text = 'tweet text'
location = 'place name'




def main():
    average = 0
    data = pd.read_csv(path, low_memory=False)
    print(f"Number of inputs : {data[text].nunique()}")
    print(f"Number of topynomns : {data.shape[0]}")

    unique_items =data[text].unique()

    total_token_length = 0
    total_items = len(unique_items)

    for item in unique_items:
        # Use regex to split the item into tokens based on whitespace or other delimiters
        tokens = item.split(' ')
        total_token_length += len(tokens)

    average_token_length = total_token_length / total_items

    print(f"Average number of tokens per input : {average_token_length}")

    toponyms_per_text = data.groupby(text)[location].nunique()
    average_toponyms_per_text = toponyms_per_text.mean()

    print("Average Toponyms per Input String:", average_toponyms_per_text)

    # Extract the text data
    text_data = data[text]

    # Tokenize the text into words
    all_tokens = [word_tokenize(text) for text in text_data]

    # Flatten the list of tokens
    all_tokens_flat = [token for tokens in all_tokens for token in tokens]

    # Calculate the vocabulary size
    vocabulary_size = len(set(all_tokens_flat))

    print("Vocabulary Size:", vocabulary_size)


main()
