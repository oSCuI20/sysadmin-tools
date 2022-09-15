#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ./endpoints/toolbox.py
#
import api

@api.route('/toolbox')
def run(method, path, query, headers, body):
  if method not in ['GET']:
    raise api.HttpMethodNotAllowed('Method ' + method + ' not allowed')

  return(200, {}, {})
         #(statuscode, Dict(headers), Dict(result))
