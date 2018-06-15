from constants import CLUSTERS_DATA, POPULAR_PRODUCTS
from httplib import HTTPSConnection
import json


def get_product_details(asin):
    url = '/api/v1/asin/' + asin
    conn = HTTPSConnection('api.barcodable.com')
    conn.request('GET', url)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data


def get_products_details():
    with open(CLUSTERS_DATA, 'r') as inputfile:
        inputfile.next()
        cluster = 0
        details = []
        for line in inputfile:
            if 'edges' in line or line == '],\n':
                break
            
            product = None
            if line[-2] == ',':
                product = eval(line.replace('true', 'True')[:-2])
            else:
                product = eval(line.replace('true', 'True')[:-1])
            
            if 'root' in product:
                print('Cluster: {}'.format(cluster))
                cluster += 1
                product_details = get_product_details(product['name'])
                product_details = eval(product_details)
                detail = {
                    'ASIN': product_details['item']['asin'],
                    'Title': product_details['item']['title'],
                    'Brand': product_details['item']['brand'],
                    'Manufacturer': product_details['item']['manufacturer'],
                    'Categories': product_details['item']['category_hierarchies']
                }
                details.append(detail)
                
        with open(POPULAR_PRODUCTS, 'w') as outfile:
            json.dump(details, outfile, indent=2)