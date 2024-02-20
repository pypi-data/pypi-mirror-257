from setuptools import setup, find_packages

VERSION = '0.2'

setup(
    name='bom-analyzer',
    version= VERSION,
    description='Bill of Materials outlier analysis using unsupervised machine learning.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'sentence_transformers',
        'matplotlib',
        'umap-learn',
        'hdbscan',
        'scikit-learn',
        'optuna',
        'tqdm'
    ]
)