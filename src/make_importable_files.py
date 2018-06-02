import csv

from constants import IMPORTABLE_EDGES
from constants import IMPORTABLE_NODES
from constants import DATASET_PATH
from product import Product


def make_importable_data():
    with open(DATASET_PATH) as inputfile:
        with open(IMPORTABLE_NODES, 'w') as outnodes:
            with open(IMPORTABLE_EDGES, 'w') as outedges:
                nodes_writer = csv.writer(outnodes)
                edges_writer = csv.writer(outedges)
                nodes_writer.writerow(['asin:ID', 'price', 'categories', ':LABEL'])
                edges_writer.writerow([':START_ID', ':END_ID', ':TYPE'])
                for line in inputfile:
                    line_dict = eval(line)
                    product = Product()
                    product.set_attributes(line_dict)
                    nodes_writer.writerow([product.asin, product.price, product.categories, 'Product'])
                    for bought in product.also_bought:
                        edges_writer.writerow([product.asin, bought, 'ALSO_BOUGHT'])


if __name__ == '__main__':
    make_importable_data()