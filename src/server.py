#!/usr/bin/env python3
import logging
import json
from src.handler.compileFirmware import *

from http.server import BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler): 
  def do_POST(self):
    if self.path != '/compileFirmware':
      return self.send_response(404)
    content_length = int(self.headers['Content-Length'])
    dataJson = self.rfile.read(content_length)
    data = json.loads(dataJson)
    binaryFile = compileFirmware(data["main"], data["header"])
    self.send_response(200)
    self.send_header('Content-Type', 'application/octet-stream')
    self.send_header('Content-Lenght', str(len(binaryFile)))
    self.end_headers()
    self.wfile.write(binaryFile)
    return