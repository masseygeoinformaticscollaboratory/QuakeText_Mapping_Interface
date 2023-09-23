import pandas as pd

embeddings_path = "../CompletedBertEmbeddings/NLPBertCompleted.csv"
coordinates_path = "../Completed_Coordinate_Data/NPLCoordinateCompleted.csv"


def main():
    embeddings_data = pd.read_csv(embeddings_path, low_memory=False)
    correct_data = pd.read_csv(coordinates_path, low_memory=False)
    print(len(embeddings_data))
    print(len(correct_data))


main()