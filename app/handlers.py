from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import base64
import cv2
import numpy as np
import  os
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            # Serve index.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('temp/index.html', 'rb') as file:
                html_content = file.read()
            self.wfile.write(html_content)
        elif self.path.startswith('/static/'):
            # Serve static files
            try:
                with open(self.path[1:], 'rb') as file:
                    content = file.read()
                self.send_response(200)
                if self.path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            # Handle other paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        if self.path == '/upload':
            print('POST request received')
            # Get the content length of the POST request
            content_length = int(self.headers['Content-Length'])
            # Parse the POST data
            post_data = self.rfile.read(content_length)
            # Extract the image data from the POST data
            _, img_data = post_data.split(b';base64,')
            img_data = base64.b64decode(img_data)
            print('Image data received')
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            
            #display detected image
            cv2.imshow('Detected Image', img)
            cv2.waitKey(0)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Image received and saved successfully')
