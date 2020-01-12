import http.server
# import urllib.parse

PORT_NUMBER = 8888


# This class will handles any incoming request from
# the browser 
class myHandler(http.server.BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !".encode('utf-8'))
        return

    # Handler for the POST requests
    def do_POST(self):
        self.send_response(200)
        if self.rfile:
            content_len = int(self.headers['Content-Length'])
            print(content_len)
            post_body_json = self.rfile.read(content_len)
            print(post_body_json)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(post_body_json)
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = http.server.HTTPServer(('', PORT_NUMBER), myHandler)
    print("Started httpserver on port ", PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
