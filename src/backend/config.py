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

FLAG_USER_ADMIN   =       # Account type admin user
FLAG_USER_NORMAL  =       # Account type normal user
FLAG_USER_TOOLBOX =       # Account type toolbox user, this is a special account
FLAG_USER_ACTIVED =       # Account is active
FLAG_USER_ENABLED =       # Account is enable use with toolbox users


TYPE_TOOLBOX_RPI     =    # Installed in RaspberryPI
TYPE_TOOLBOX_BPI     =    # Installed in BananaPi
TYPE_TOOLBOX_BPI_R2  =    # Installed in BananaPi Router v2 model
TYPE_TOOLBOX_VM      =    # Installed in Virtual Machine
TYPE_TOOLBOX_UNKNOWN =    # Installed in unknown system
