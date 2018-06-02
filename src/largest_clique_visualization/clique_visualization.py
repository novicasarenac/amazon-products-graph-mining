import SimpleHTTPServer
import SocketServer


PORT = 9300


def visualize_clique():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(('', PORT), Handler)
    print('\n===> To show visualization visit: localhost:9300/largest_clique_visualization/static/largest_clique_visualization.html\n')
    httpd.serve_forever()