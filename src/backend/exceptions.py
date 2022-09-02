# -*- coding: utf-8 -*-
#
# ./exceptions.py
#
class HttpBadRequest(Exception):
  code = 400

class HttpUnauthorized(Exception):
  code = 401

class HttpForbidden(Exception):
  code = 403

class HttpNotFound(Exception):
  code = 404

class HttpMethodNotAllowed(Exception):
  code = 405

class HttpNotAcceptable(Exception):
  code = 406

class HttpNotImplement(Exception):
  code = 501

class HttpServiceUnavailable(Exception):
  code = 503
