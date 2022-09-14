# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/constants.py
# Eduardo Banderas Alba
# 2022-08
#

class Constants(object):

  PATHLIB  = 'libs.pcap.layer'

  DATALINK     = [ 'arp' ]  #arp
  NETWORK      = [ 'ipv4' ]
  TRANSPORT    = [ 'udp', 'tcp', 'icmp', 'igmp']
  SESSION      = [ ]
  PRESENTATION = [ ]
  APPLICATION  = [ 'dhcp', 'dns', 'http', 'https', 'ftp']
#class Constants
