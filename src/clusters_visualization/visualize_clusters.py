import SimpleHTTPServer
import SocketServer


PORT = 9200


def visualize_clusters():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(('', PORT), Handler)
    print('\n===> To show visualization visit: localhost:9200/clusters_visualization/template/clusters_visualization.html\n')
    httpd.serve_forever()