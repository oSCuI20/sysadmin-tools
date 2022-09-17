# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/constants.py
# Eduardo Banderas Alba
# 2022-08
#

class Constants(object):

  PATHLIB  = 'libs.pcap.layer'

  DATALINK     = [ 'ARP' ]  #arp
  NETWORK      = [ 'IPv4' ]
  TRANSPORT    = [ 'UDP', 'TCP', 'ICMP', 'IGMP']
  SESSION      = [ ]
  PRESENTATION = [ ]
  APPLICATION  = [ 'DHCP', 'DNS', 'HTTP', 'HTTPS', 'FTP']
#class Constants
