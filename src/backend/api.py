# -*- coding: utf-8 -*-
#
# ./api.py
#
import sys
import json
import http.client
from exceptions import (HttpBadRequest, HttpUnauthorized, HttpForbidden,
                        HttpNotFound, HttpMethodNotAllowed, HttpNotAcceptable,
                        HttpNotImplement, HttpServiceUnavailable)

_endpoint = {}

def route(path):
  def inner(fun):
    _endpoint[path] = fun
    return fun
  return inner
#route


def run(method, path, query, headers, body, debug):
  request = {
    'method': method,
    'path': path,
    'query': query,
    'headers': headers,
    'body': body
  }

  oheaders = {}
  out = ''

  try:
    for q in query:
      if len(query[q]) > 1:
        raise HttpBadRequest('Multiple values in url')

      query[q] = query[q][0]
    #endfor

    if path not in _endpoint:
      raise HttpUnauthorized(f'Not found endpoint {path}')

    (code, oheaders, out) = _endpoint[path](**request)

  except Exception as err:
    code = 403 if not hasattr(err, 'code') else err.code
    out  = HttpExceptionHandler(code, err, request, debug)

  return HttpResponsesHandler(code, oheaders, out, debug)
#run


def HttpResponsesHandler(code=200, headers={}, out='', debug=False):
  if isinstance(out, dict) or isinstance(out, list):
    if debug:    out = json.dumps(out, indent=2)
    else:        out = json.dumps(out)

  out += '\n'
  h = (f'Status: {code} {http.client.responses[code]}\r\n' +
       f'Content-Length: {len(str(out))}\r\n' +
       f'Content-Type: application/json; charset=utf-8\r\n')

  for head in headers.keys():
    h += f'{head}: {headers[head]}\r\n'

  h += '\r\n'

  sys.stdout.write(f'{h}{out}')
  sys.stdout.flush()

  return code
#HttpResponsesHandler


def HttpExceptionHandler(code, err, request, debug):
  if debug:
    err = {
      'Status': code,
      'reason': {
        'code':    code,
        'err':     str(print_debug(err)),
        'request': request
      }
    }

  else:
    err = ''

  return err
#HttpExceptionHandler


def print_debug(err):
  return ((f'Error on line {sys.exc_info()[-1].tb_lineno}', type(err).__name__, err))
#print_debug
