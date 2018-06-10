from constants import CLUSTERS_DATA
from httplib import HTTPSConnection


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
        for line in inputfile:
            if 'edges' in line or line == '],\n':
                break
            
            product = None
            if line[-2] == ',':
                product = eval(line.replace('true', 'True')[:-2])
            else:
                product = eval(line.replace('true', 'True')[:-1])
            
            if 'root' in product:
                product_details = get_product_details(product['name'])
                product_details = eval(product_details)
                print('Product ASIN: {}'.format(product_details['item']['asin']))
                print('Product Title: {}'.format(product_details['item']['title']))
                print('Product Brad: {}'.format(product_details['item']['brand']))
                print('Product Manufacturer: {}'.format(product_details['item']['manufacturer']))
                print('Product Categories: {}\n\n'.format(product_details['item']['category_hierarchies']))
