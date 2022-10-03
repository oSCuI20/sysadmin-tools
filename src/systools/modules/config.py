# -*- coding: utf-8 -*-
#
# ./modules/config.py
# Eduardo Banderas Alba
# 2022-09
#
# Set default config
#

class Config:
  logger = {
    'default'   : '/var/log/sysadmins-tools/sysadmins.log',
    'device'    : '/var/log/sysadmins-tools/device.log',
    'netstatus' : '/var/log/sysadmins-tools/netstatus.log',
    'netscanner': '/var/log/sysadmins-tools/netscanner.log'
  }

  endpoint = 'http://my-domain-example.com/systools'

  delay = {
    'netstatus': 3600,
    'netscanner': 7200
  }

  pidpath = './pidfiles'
#class Config
