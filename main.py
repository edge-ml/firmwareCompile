#!/usr/bin/env python3
import time
from http.server import HTTPServer
from src.server import Server
import logging
import threading, socket, socketserver
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000
THREAD_COUNT = 4


addr = ('', PORT_NUMBER)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
# maximum backlog for incoming connections
sock.listen(20)

# Launch listener threads.
class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.daemon = True
        self.start()
    def run(self):
        httpd = HTTPServer(addr, Server, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        httpd.socket = sock
        httpd.server_bind = self.server_close = lambda self: None

        httpd.serve_forever()
print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))        
[Thread(i) for i in range(THREAD_COUNT)]
time.sleep(9e9)

#if __name__ == '__main__':
#    logging.basicConfig(level=logging.INFO)
#    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
#    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
#    try:
#        httpd.serve_forever()
#    except KeyboardInterrupt:
#        pass
#    httpd.server_close()
#    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))