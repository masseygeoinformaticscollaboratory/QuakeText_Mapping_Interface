import numpy as np
import pandas as pd


def main():
    dataset_1 = pd.read_csv("Georgia50.csv", low_memory=False)
    dataset_1['True/False'] = dataset_1['True/False'].fillna(0)
    dataset_2 = pd.read_csv("Sophie50.csv", low_memory=False)
    dataset_2 = dataset_2.drop('Unnamed: 5', axis=1)
    dataset_2['True/False'] = dataset_2['True/False'].fillna(0)

    num_ratings = len(dataset_2)
    yes_yes = 0
    yes_no = 0
    no_yes = 0
    no_no = 0

    for index, (row1, row2) in enumerate(zip(dataset_1.iterrows(), dataset_2.iterrows())):
        row_1_value = row1[1]['True/False']
        row_2_value = row2[1]['True/False']

        if row_1_value == 1 and row_2_value == 1:
            yes_yes += 1

        elif row_1_value == 1 and row_2_value == 0:
            yes_no += 1

        elif row_1_value == 0 and row_2_value == 1:
            no_yes += 1

        elif row_1_value == 0 and row_2_value == 0:
            no_no += 1

    print(f"Yes Yes {yes_yes}")
    print(f"Yes No {yes_no}")
    print(f"No Yes {no_yes}")
    print(f"No No {no_no}")

    p_0 = (yes_yes + no_no) / num_ratings
    p_Yes = ((yes_yes + yes_no) / num_ratings) * ((yes_yes + no_yes) / num_ratings)
    p_No = ((no_yes + no_no) / num_ratings) * ((yes_no + no_no) / num_ratings)
    p_e = p_Yes + p_No
    K = (p_0 - p_e) / (1 - p_e)
    print(f'Cohen’s Kappa: {K}')


main()
