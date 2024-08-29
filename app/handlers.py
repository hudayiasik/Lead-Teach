from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import base64
import cv2
import numpy as np
import  os
import requests
from utils import image_processing

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
        elif self.path == '/image':
            # Serve the processed grayscale image
            try:
                with open('images/gray_image.jpg', 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Image not found')
        else:
            # Handle other paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        if self.path == '/upload':
        
            try:
                # Extract image data from POST request
                img_data = self._extract_image_data()

                # Process image using imageprocessing.py
                liste,contour_img = image_processing.process_image(img_data)

                # Save processed image
                self._save_image(contour_img)
                print(liste)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(liste.encode())
            except Exception as e:
                print(f"Error processing image: {e}")
                self.send_error(500, 'Internal server error')

    def _extract_image_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        _, img_data = post_data.split(b';base64,')
        img_data = base64.b64decode(img_data)
        return img_data

    def _save_image(self, img):
        cv2.imwrite('images/gray_image.jpg', img)