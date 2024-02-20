from optuna.samplers import TPESampler
import umap.umap_ as umap
from hdbscan import HDBSCAN
import optuna
import numpy as np


# calculates the best parameters for clustering and dimension reduction
def optimize_hyperparameters(data: np.ndarray, seed: int, trials: int = 50) -> dict:
    sampler = TPESampler(seed=seed)
    study = optuna.create_study(sampler=sampler, direction='maximize')
    study.optimize(lambda trial: objective_function(trial, data, seed), n_trials=trials)
    return study.best_params


# runs umap and hdbscan with a set of parameters
# returns the validity score of the run
def objective_function(trial, data: np.ndarray, seed: int) -> float:
    min_cluster_size = trial.suggest_int('min_cluster_size', 2, 100)
    min_samples = trial.suggest_int('min_samples', 1, 100)
    alpha = trial.suggest_float('alpha', 0.0, 2.0)
    n_neighbors = trial.suggest_int('n_neighbors', 2, 700)
    min_dist = trial.suggest_float('min_dist', 0.0, 0.99)

    umap_data = umap.UMAP(n_components=2,
                          n_neighbors=n_neighbors,
                          min_dist=min_dist,
                          random_state=seed,
                          n_jobs=1).fit_transform(data)

    hdb = HDBSCAN(min_cluster_size=min_cluster_size,
                  min_samples=min_samples,
                  alpha=alpha,
                  gen_min_span_tree=True)

    hdb.fit(umap_data)
    return hdb.relative_validity_
