#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ./endpoints/devices.py
#
import api

@api.route('/devices')
def run(method, path, query, headers, body):
  if method not in ['GET']:
    raise api.HttpMethodNotAllowed('Method ' + method + ' not allowed')

  return(200, {}, {})
         #(statuscode, Dict(headers), Dict(result))


@api.route('/device')
def run(method, path, query, headers, body):
  return(200, {}, {})
