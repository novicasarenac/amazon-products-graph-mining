import igraph as ig
import numpy as np

from py2neo import Graph
from constants import CLUSTERS_DATA, CLIQUE_DATA


class GraphManager():
    def __init__(self):
        self.graph = ig.Graph()
        self.graph_database = Graph(password='admin')
        self.read_nodes()
        self.read_edges()
        self.find_clusters()
        self.find_largest_clique()

    def read_nodes(self):
        print('===> Reading nodes\n')
        # only products that have relationships with at least one another product
        query = 'match (p:Product)-[:ALSO_BOUGHT]-(:Product) \
        return distinct p.asin as asin, p.categories as categories'
        result = self.graph_database.run(query)
        for node in result:
            self.graph.add_vertex(node['asin'], categories=node['categories'])
        print('===> Read {} nodes\n'.format(self.graph.vcount()))

    def read_edges(self):
        print('===> Reading edges\n')
        query = 'match (p1:Product)-[:ALSO_BOUGHT]->(p2:Product) \
        return p1.asin as asin1, p2.asin as asin2'
        result = self.graph_database.run(query)
        for relationship in result:
            self.graph.add_edge(relationship['asin1'], relationship['asin2'])
        print('===> Read {} edges\n'.format(self.graph.ecount()))

    def find_clusters(self):
        print('===> Performing clustering\n')
        clusters = self.graph.community_edge_betweenness(directed=False)
        clusters = clusters.as_clustering()
        subgraph_vertices = []
        with open(CLUSTERS_DATA, 'w') as outfile:
            # nodes
            outfile.write("{ \"nodes\": [\n")
            for index in range(0, 10):
                print('Cluster: {}'.format(index))
                counter = 0
                cluster = clusters[index]
                # max degree in cluster
                current_cluster = [self.graph.vs[member]['name'] for member in cluster]
                degrees = self.graph.degree(current_cluster)
                max_degree_index = np.argmax(degrees)
                max_degree_node_id = current_cluster[max_degree_index]

                for member in cluster:
                    counter += 1
                    node = self.graph.vs[member].attributes()
                    if node['name'] == max_degree_node_id:
                        node['root'] = True
                    else:
                        node['cluster'] = index
                    node['id'] = node['name']
                    subgraph_vertices.append(node['name'])
                    if counter < len(cluster) or index < 9:
                        json_data = json.dumps(node) + ','
                    else:
                        json_data = json.dumps(node)
                    outfile.write(json_data)
                    outfile.write('\n')
            outfile.write("],\n")

            #edges
            outfile.write("\"edges\": [\n")
            subgraph = self.graph.subgraph(subgraph_vertices)
            counter = 0
            for single_edge in subgraph.es:
                counter += 1
                vertices = single_edge.tuple
                edge = {}
                edge['source'] = subgraph.vs[vertices[0]]['name']
                edge['target'] = subgraph.vs[vertices[1]]['name']
                if counter < subgraph.ecount():
                    json_data = json.dumps(edge) + ','
                else:
                    json_data = json.dumps(edge)
                outfile.write(json_data)
                outfile.write('\n')
            outfile.write("] }\n")
    
    def find_largest_clique(self):
        print('===> Finding largest clique\n')
        with open(CLIQUE_DATA, 'w') as outfile:
            largest_clique = self.graph.largest_cliques()[0]
            nodes_number = len(largest_clique)
            counter = 0
            outfile.write("{ \"nodes\": [\n")
            subgraph_vertices = []
            for member in largest_clique:
                counter += 1
                node = self.graph.vs[member].attributes()
                node['id'] = node['name']
                subgraph_vertices.append(node['name'])
                if counter < nodes_number:
                    json_data = json.dumps(node) + ','
                else:
                    json_data = json.dumps(node)
                outfile.write(json_data)
                outfile.write('\n')
            outfile.write("],\n")

            outfile.write("\"edges\": [\n")
            subgraph = self.graph.subgraph(subgraph_vertices)
            counter = 0
            for single_edge in subgraph.es:
                counter += 1
                vertices = single_edge.tuple
                edge = {}
                edge['source'] = subgraph.vs[vertices[0]]['name']
                edge['target'] = subgraph.vs[vertices[1]]['name']
                if counter < subgraph.ecount():
                    json_data = json.dumps(edge) + ','
                else:
                    json_data = json.dumps(edge)
                outfile.write(json_data)
                outfile.write('\n')
            outfile.write("] }\n")