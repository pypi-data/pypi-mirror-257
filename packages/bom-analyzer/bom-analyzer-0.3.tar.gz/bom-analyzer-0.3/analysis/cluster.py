from umap.umap_ import UMAP
from hdbscan import HDBSCAN
import numpy as np

'''
param_dict is formatted in the same way as the optimizer,
shoud look like this

   param_dict = {
        'min_cluster_size': 48,
        'min_samples': 16,
        'alpha': 0.9615277268640865,
        'n_neighbors': 598,
        'min_dist': 0.9483669074161485
    }

'''


# generate representative 2D vector space from sentence embeddings
# takes a numpy array and dictionary of hyperparameters as input
# returns the original numpy array reduced to 2-dimensions
def dimension_reduction(st_data: np.ndarray, param_dict: dict, seed: int) -> np.ndarray:
    return UMAP(n_components=2,
            n_neighbors=param_dict['n_neighbors'],
            random_state=seed,
            min_dist=param_dict['min_dist'],
            n_jobs=1).fit_transform(st_data)


# acquire ordered cluster labels via HDBSCAN
# takes a 2d numpy array and dictionary of hyperparameters as input
# returns a numpy array of labels, corresponding to the
# cluster each datapoint is associated with
def clustering(umap_data: np.ndarray, param_dict: dict) -> np.ndarray:
    hdb = HDBSCAN(min_cluster_size=param_dict['min_cluster_size'],
            min_samples=param_dict['min_samples'],
            alpha=param_dict['alpha'],
            gen_min_span_tree=True)

    return hdb.fit_predict(umap_data)
