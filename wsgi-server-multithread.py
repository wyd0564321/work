'''wsgi-server.py'''

import socket
from io import StringIO
import sys
import threading
#import time

class client(threading.Thread):
    def __init__(self,conn,addr,ser_name,port,app):
        threading.Thread.__init__(self)
        self.client_connection=conn
        self.addr=addr
        self.application=app
        self.server_name=ser_name
        self.thread_stop=False
        self.headers_set=[]
        self.server_port=port

    def run(self):
        self.handle_one_request()
        self.stop()

    def stop(self):
        self.thread_stop= True
     
    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024).decode()

        if(len(request_data)!=0):
            print(''.join(
                '< {line}\n'.format(line=line)
                for line in request_data.splitlines()
            ))
 
            self.parse_request(request_data)
 
            # Construct environment dictionary using request data
            env = self.get_environ()
 
            # It's time to call our application callable and get
            # back a result that will become HTTP response body
            result = self.application(env, self.start_response)
     
            # Construct a response and send it back to the client
            self.finish_response(result)
            #time.sleep(10)
            #print('im finished')
 
    def parse_request(self, text):
        request_lines = text.splitlines()

        if(len(request_lines)>0):
            request_line = request_lines[0]
            request_line = request_line.rstrip('\r\n')
            # Break down the request line into components
            (self.request_method,  # GET
             self.path,            # /hello
             self.request_version  # HTTP/1.1
             ) = request_line.split()
 
    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 3333
        return env
 
    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response
 
    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response.encode())
        finally:
            self.client_connection.close()
    
class WSGIServer(): 
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
 
    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(self.request_queue_size)
        #listen_socket.listen()
        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
 
    def set_app(self, application):
        self.application = application
 
    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()

            c = client(self.client_connection,client_address,
                       self.server_name,self.server_port,self.application)
            c.start()
 
SERVER_ADDRESS = (HOST, PORT) = '', 3333
 
 
def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server
 
 
if __name__ == '__main__':
    app_path = 'application:app'
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()
