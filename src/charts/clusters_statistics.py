import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec
from constants import CLUSTERS_DATA


class ClusterCategories():
    def __init__(self, cluster_number):
        self.cluster_number = cluster_number
        self.categories = {}
    
    def add_category(self, category_name):
        if category_name in self.categories:
            self.categories[category_name] += 1
        else:
            self.categories[category_name] = 1
    
    def get_data_for_chart(self, categories_colors):
        labels = self.categories.keys()
        sizes = self.categories.values()
        colors = [categories_colors[label] for label in labels]
        return labels, sizes, colors


def plot_clusters_statistics():
    clusters, all_categories = read_clusters_and_categories()
    categories_colors = dict(zip(all_categories, mcolors.XKCD_COLORS))

    grid = GridSpec(2, len(clusters) / 2 + 2)
    for i, cluster in enumerate(clusters):
        if i < len(clusters) / 2:
            plt.subplot(grid[0, i], aspect=1)
        else:
            plt.subplot(grid[1, i - len(clusters) / 2], aspect=1)
        labels, sizes, colors = cluster.get_data_for_chart(categories_colors)
        plt.pie(sizes, colors=colors, autopct=custom_autopct, shadow=True)
        plt.axis('equal')
    patchList = []
    for key in categories_colors:
        data_key = mpatches.Patch(color=categories_colors[key], label=key)
        patchList.append(data_key)
    plt.legend(handles=patchList, loc=1, bbox_to_anchor=(2.5, 2), ncol=2)
    plt.show()


def custom_autopct(pct):
    return ('%.2f%%' % pct) if pct > 10 else ''


def read_clusters_and_categories():
    clusters = []
    all_categories = []
    with open(CLUSTERS_DATA, 'r') as inputfile:
        inputfile.next()
        for line in inputfile:
            if 'edges' in line or line == '],\n':
                break
            
            product = None
            if line[-2] == ',':
                product = eval(line.replace('true', 'True')[:-2])
            else:
                product = eval(line.replace('true', 'True')[:-1])
            
            if len(filter(lambda x: x.cluster_number == product['cluster'], clusters)) == 0:
                clusters.append(ClusterCategories(product['cluster']))
            cluster = filter(lambda x: x.cluster_number == product['cluster'], clusters)[0]

            categories = eval(product['categories'])
            if len(categories) > 1:
                cluster.add_category(categories[1])
                if categories[1] not in all_categories:
                    all_categories.append(categories[1])
        
        for cluster in clusters:
            print('\n\n===> Cluster {}'.format(cluster.cluster_number))
            for category, cat_count in cluster.categories.iteritems():
                print('{}: {}'.format(category, cat_count))
    return clusters, all_categories
