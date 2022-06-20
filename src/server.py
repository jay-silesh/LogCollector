from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        path = query_components["path"]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "From new server the log path is /var/log/%s" % path
        self.wfile.write(bytes(message, "utf8"))


with HTTPServer(('', 8000), handler) as server:
    print("Starting server on 8000")
    server.serve_forever()
