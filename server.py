from http.server import HTTPServer, BaseHTTPRequestHandler
from app.handlers import MyHandler
import socket

def run_server(host='192.168.1.65', port=9000):
    host = socket.gethostbyname(socket.gethostname()) # Get the IP address of the current machine
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server running on http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
