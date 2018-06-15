import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = BASE_DIR + '/data/meta_Apps_for_Android.json'
IMPORTABLE_NODES = BASE_DIR + '/data/nodes.csv'
IMPORTABLE_EDGES = BASE_DIR + '/data/edges.csv'
CLUSTERS_DATA = BASE_DIR + '/clusters_visualization/template/clusters.json'
CLIQUE_DATA = BASE_DIR + '/largest_clique_visualization/template/clique.json'
SUBGRAPH_DATA = BASE_DIR + '/clusters_visualization/template/subgraph_clusters.json'
POPULAR_PRODUCTS = BASE_DIR + '/data/popular.json'