#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ./index.py
#
import sys
import os
import json
import http.client
from urllib.parse import parse_qs

import api

from endpoints  import *
from config     import cfg


def main():
  method  = os.environ.get('REQUEST_METHOD', 'GET').upper()
  path    = os.environ.get('PATH_INFO', '/').rstrip('/')
  path    = path or '/'
  query   = parse_qs(os.environ.get('QUERY_STRING', ''))
  headers = {
    'Content-Type': os.environ.get('CONTENT_TYPE', ''),
    'Content-Length': os.environ.get('CONTENT_LENGTH', 0),
  }
  body = {}



  if headers.get('Content-Length'):
    try:
      if method == 'OPTIONS':
        sys.stdout.write(
          "Allow: GET, POST, PUT, DELETE\r\n" +
          "Access-Control-Allow-Origin: *\r\n" +
          "Access-Control-Expose-Headers: Token\r\n" +
          "Access-Control-Allow-Method: GET, POST, PUT, DELETE\r\n" +
          "Content-Type: application/json; charset=utf-8\r\n" +
          "Accept: application/json\r\n" +
          "Status: 200 " + http.client.responses[200] + "\r\n\r\n" +
          ""
        )
        sys.exit(0)

      if headers.get('Content-Type', '').find('application/json') == -1:
        raise Exception('Force exception')

      if int(headers['Content-Length']) > 0:
        body = json.loads(sys.stdin.read(int(headers['Content-Length'])))

    except:
      status = 406
      oheaders = { 'Status': status }
      err = api.HttpExceptionHandler(406, "Invalid JSON format", method, path, query, oheaders, body, cfg.DEBUG)
      sys.exit(err)

  err = api.run(method, path, query, headers, body, cfg.DEBUG)
  sys.exit(err if err != 200 else 0)
#main


if __name__ == '__main__':
  try:    reload(sys); sys.setdefaultencoding("utf8")
  except: pass

  #Servidor de test para depuración (NO USAR EN PRODUCCIÓN):
  if len(sys.argv) > 1 and sys.argv[1] == "-d":
    del sys.argv[1:2]
    import http.server
    class RunTestServer(http.server.CGIHTTPRequestHandler):
      def do_PUT(self): self.do_POST()
      def do_PATCH(self): self.do_POST()
      def do_DELETE(self): self.do_POST()
      def is_cgi(self):
        self.cgi_info = (os.path.dirname(sys.argv[0]),
                         os.path.basename(sys.argv[0]) + self.path)

        return True
      #is_cgi
    #class RunTestServer
    try:
      http.server.test(RunTestServer)
    except KeyboardInterrupt: #Ej: Ctrl+C o SIGINT
      sys.stderr.write("\nServer stopped.\n")
      sys.exit(0)

  main()
