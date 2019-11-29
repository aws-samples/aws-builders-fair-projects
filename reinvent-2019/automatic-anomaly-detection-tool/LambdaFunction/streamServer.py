import io
import socket
import struct
import cv2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import time
import urllib2
import urlparse

FILE_PATH = '/tmp/bfsushi/detected.jpg'


class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print 'path:' + self.path
        o = urlparse.urlparse(self.path)
        if o.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header(
                'Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            last_size = 0
            while True:
                img = cv2.imread(FILE_PATH)
                if img is None:
                    continue
                r, buf = cv2.imencode(".jpg", img)
                new_size = len(buf)
                if new_size == last_size:
                    self.wfile.write("--jpgboundary\r\n")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(buf)))
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                    self.wfile.write('\r\n')
                else:
                    last_size = new_size


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    try:
        server = ThreadedHTTPServer(('', 9090), StreamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    main()
