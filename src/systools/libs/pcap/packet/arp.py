# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/arp.py
# Eduardo Banderas Alba
# 2022-08
#
# arp packet building
#
from . import EtherPacket

from struct import pack


class ARPPacket(object):

  __RAW_LEN = 28

  __htype = pack('!H', 0x01)    #2 bytes  hardware type
  __ptype = pack('!H', 0x0800)  #2 bytes  protocol type
  __hlen  = pack('!B', 0x06)    #1 byte   hardware length
  __plen  = pack('!B', 0x04)    #1 byte   protocol length
  __op    = None                #2 bytes  op code
  __sha   = None                #6 bytes  sender hardware address
  __spa   = None                #4 bytes  sender protocol address
  __tha   = None                #6 bytes  target hardware address
  __tpa   = None                #4 bytes  target protocol address

  ethertype = 0x0806

  def __init__(self, target, sender):
    self.tha = target['hwaddr']
    self.sha = sender['hwaddr']
    self.tpa = target['ipaddr']
    self.spa = sender['ipaddr']

    self.ether = EtherPacket(target['hwaddr'], sender['hwaddr'], self.ethertype)
  #__init__

  def __raw(self):
    return self.ether.raw + \
           self.htype + self.ptype + self.hlen + self.plen + self.op + \
           self.sha + self.spa + self.tha + self.tpa
  #raw

  @property
  def raw_request(self):
    self.__op = 0x01
    return self.__raw()
  #raw_request

  @property
  def raw_reply(self):
    self.__op = 0x02
    return self.__raw()
  #raw_reply

  @property
  def htype(self):
    return self.__htype
  #htype

  @property
  def ptype(self):
    return self.__ptype
  #ptype

  @property
  def hlen(self):
    return self.__hlen
  #hlen

  @property
  def plen(self):
    return self.__plen
  #plen

  @property
  def op(self):
    return pack('!H', self.__op)
  #op

  @property
  def sha(self):
    return self.__sha

  @sha.setter
  def sha(self, v):
    self.__sha = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
  #sha

  @property
  def tha(self):
    return self.__tha

  @tha.setter
  def tha(self, v):
    self.__tha = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
  #tha

  @property
  def spa(self):
    return self.__spa

  @spa.setter
  def spa(self, v):
    self.__spa = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #spa

  @property
  def tpa(self):
    return self.__tpa

  @tpa.setter
  def tpa(self, v):
    self.__tpa = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #tpa
#class ARPPacket
