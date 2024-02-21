import pandas as pd

def data_import(file_path):
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]
    print(df.columns)
    return df
