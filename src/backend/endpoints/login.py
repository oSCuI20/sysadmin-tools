#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ./endpoints/login.py
#
import api

@api.route('/login')
def run(method, path, query, headers, body):
  if method not in ['GET']:
    raise api.HttpMethodNotAllowed('Method ' + method + ' not allowed')

  return(200, {}, {})
         #(statuscode, Dict(headers), Dict(result))


@api.route('/logout')
def run(method, path, query, headers, body):
  return(200, {}, {})
