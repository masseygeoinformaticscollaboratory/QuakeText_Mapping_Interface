import pandas as pd
from pathlib import Path
import chardet


def read_data():
    path = 'NPL_Data'
    files = Path(path).glob('*.csv')
    dfs=[]
    for f in files:
        try:
            df = pd.read_csv(f, encoding='macroman')
            dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f"The file {f} is empty or has no columns to parse.")
    print(dfs)


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


read_data()