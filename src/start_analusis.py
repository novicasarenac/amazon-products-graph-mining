import sys
import argparse

from graph_analyze import GraphManager
from clusters_visualization.visualize_clusters import visualize_clusters
from largest_clique_visualization.clique_visualization import visualize_clique
from charts.clusters_statistics import plot_clusters_statistics
from products_details import get_products_details


def perform_actions():
    ap = argparse.ArgumentParser()
    ap.add_argument('-vc', '--visualize-clusters', required=False, help='Run web server with clusters view')
    ap.add_argument('-vlc', '--visualize-largest-clique', required=False, help='Visualize largest clique at graph')
    ap.add_argument('-ag', '--analyze-graph', required=False, help='Run graph analyzer')
    ap.add_argument('-cs', '--clusters-statistics', required=False, help='Plots clusters statistics')
    ap.add_argument('-pd', '--products-details', required=False, help='Shows the most popular products details')

    args = vars(ap.parse_args())
    if args['visualize_clusters']:
        print('===> Visualizing clusters')
        visualize_clusters()
    elif args['visualize_largest_clique']:
        print('===> Visualizing largest clique at graph')
        visualize_clique()
    elif args['analyze_graph']:
        print('===> Performing graph analyzis')
        graph_manager = GraphManager()
    elif args['clusters_statistics']:
        print('===> Plotting clusters statistics')
        plot_clusters_statistics()
    elif args['products_details']:
        print('===> Getting the most popular products details')
        get_products_details()


if __name__ == '__main__':
    perform_actions()