import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# preprocesses the data to be taken as input
# returns it as a numpy array of strings
# (could have kept using a dataframe, but numpy is easier for next steps)
def preprocess(csv_path: str) -> np.ndarray:
    bom = pd.read_csv(csv_path, header=0, low_memory=False)

    # Replace NaN values with a placeholder string,
    # '#' made sense to me since it doesn't appear anywhere
    # else in the data
    bom = bom.fillna("#")\
        .drop('SERNUM', axis='columns')\
        .drop('HWRMA', axis='columns')
    arr = bom.astype(str).to_numpy()
    return arr


# converts strings into numerical weights
# uses HuggingFace Sentence Transformers
def sentence_transform(data: np.ndarray, device: str) -> np.ndarray:
    product_strings = [''.join(row) for row in data]
    model_gte_large = SentenceTransformer('thenlper/gte-large')
    st_data = model_gte_large.encode(product_strings, show_progress_bar=True, device=device)
    return st_data
