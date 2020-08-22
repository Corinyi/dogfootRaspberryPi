################################
##Generated with a lot of love##
##    with   EasyPython       ##
##Web site: easycoding.tn     ##
################################
from http.server import BaseHTTPRequestHandler, HTTPServer
import random

request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request
    #messagetosend = bytes((str((random.randint(1, 100)))),"utf")
    messagetosend = bytes((str(1)),"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    return


server_address_httpd = ('192.168.0.142',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting server')
httpd.serve_forever()

'hello world'

self.requestline

print('abc')

#request = [5 : int(len()-9)]
request = request[5 : int(len(request)-9)]
print(request)

self.requestline
