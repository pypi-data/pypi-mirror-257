import pandas as pd

def leos_dataset(endpoint):
    return pd.read_json(endpoint)
