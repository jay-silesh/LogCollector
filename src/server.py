from http.server import BaseHTTPRequestHandler, HTTPServer


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "From new server"
        self.wfile.write(bytes(message, "utf8"))


with HTTPServer(('', 8000), handler) as server:
    print("Starting server on 8000")
    server.serve_forever()
