################################
##Generated with a lot of love##
##    with   EasyPython       ##
##Web site: easycoding.tn     ##
################################
from http.server import BaseHTTPRequestHandler, HTTPServer

request = None
text = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request, text
    messagetosend = bytes('hello world',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    request = self.requestline
    request = text[5 : int(len(text)-9)]
    return


server_address_httpd = ('192.168.1.5',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('starting server')
httpd.serve_forever()
