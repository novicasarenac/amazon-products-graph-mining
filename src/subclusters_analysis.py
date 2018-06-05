import igraph as ig
import numpy as np
import json

from constants import SUBGRAPH_DATA


class SubclusterAnalysis():
    def __init__(self, subgraph):
        print('===> Subgraph created \n')
        self.graph = subgraph
    
    def analuze(self):
        print('===> Performing clustering on subgraph\n')
        clusters = self.graph.community_leading_eigenvector(clusters=10)
        print('===> Total clusters: {} \n'.format(len(clusters)))
        subgraph_vertices = []

        with open(SUBGRAPH_DATA, 'w') as outfile:
            # nodes
            outfile.write("{ \"nodes\": [\n")
            for index in range(0, len(clusters)):
                counter = 0
                cluster = clusters[index]
                print('Subcluster {} size: {} \n'.format(index, len(cluster)))
                # max degree in subcluster
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
                    if counter < len(cluster) or index < (len(clusters) - 1):
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
        return True