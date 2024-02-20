import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
from threading import Thread
from socket_server import SocketServer
from http import HTTPStatus

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', HTTPStatus.NOT_FOUND)

    def send_html_file(self, filename, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(HTTPStatus.OK)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers() 
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        
        socket_server.process_data(data_dict)

        self.send_response(HTTPStatus.FOUND)
        self.send_header('Location', '/')
        self.end_headers()

def run_http_server():
    server_address = ('', 3000)
    http_server = HTTPServer(server_address, HttpHandler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

if __name__ == '__main__':
    
    socket_server = SocketServer() 
    http_thread = Thread(target=run_http_server) 
    socket_thread = Thread(target=socket_server.run)  
    
    http_thread.start()
    socket_thread.start()

    http_thread.join()
