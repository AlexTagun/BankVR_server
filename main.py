import http.server
from DataBase import DataBase

PORT_NUMBER = 8081

def is_settings():
    return "{\"Version\": \"0.0.1\", \"Server\": \"http://localhost:8081\"}"

get_request_handler = {
    "/is/settings": is_settings
}

def uuid_create(data):
    return "{\"requestTime\": 123, \"code\": 0, \"msg\": \"message\", \"payload\": \"payload_string\"}"

def register(data):
    return "{\"requestTime\": 123, \"code\": 0, \"msg\": \"message\"}"

def login(data):
    return "{\"requestTime\": 123, \"code\": 0, \"msg\": \"message\", \"payload\": {\"token\": \"token_data\"}}"

post_request_handler = {
    "/uuid/create": uuid_create,
    "/register": register,
    "/login": login
}


# This class will handles any incoming request from
# the browser 
class myHandler(http.server.BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = get_request_handler[self.path]()
        print(response)
        
        # Send the html message
        self.wfile.write(response.encode('utf-8'))
        return

    # Handler for the POST requests
    def do_POST(self):
        self.send_response(200)
        if self.rfile:
            content_len = int(self.headers['Content-Length'])
            print(content_len)
            post_body_json = self.rfile.read(content_len)
            print(post_body_json)
            
            responce = post_request_handler[self.path](post_body_json)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(responce.encode('utf-8'))
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = http.server.HTTPServer(('', PORT_NUMBER), myHandler)
    print("Started httpserver on port ", PORT_NUMBER)

    db = DataBase()
    db.ExecuteQuery()
    
    # Wait forever for incoming htto requests
    server.serve_forever()
    
    

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
