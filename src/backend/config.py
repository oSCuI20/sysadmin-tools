# -*- coding: utf-8 -*-
#
# ./config.py
#


class cfg:
  DEBUG = True    #Modo depuración

  secrets = {
    'pass': '',
    'jwt': ''
  }
  
  db = {
    "host":  '172.16.80.10',
    "port":   3306,
    "user":   'mysql',
    "passwd": 'password',
    "db":     'SysAdminTools',
    "charset": "utf8"
  }
#class cfg
