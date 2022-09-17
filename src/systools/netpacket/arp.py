# -*- coding: utf-8 -*-
#
# ./netpacket/arp.py
# Eduardo Banderas Alba
# 2022-08
#
# ARP Packet
#
from struct import pack


class ARPPacket(object):

  # Ethernet
  __dst       = None   #6 bytes
  __src       = None   #6 bytes
  __ethertype = pack('!H', 0x0806)   #2 bytes

  # ARP
  __htype = pack('!H', 0x01)    #2 bytes  hardware type
  __ptype = pack('!H', 0x0800)  #2 bytes  protocol type
  __hlen  = pack('!B', 0x06)    #1 byte   hardware length
  __plen  = pack('!B', 0x04)    #1 byte   protocol length
  __op    = None                #2 bytes  op code
  __sha   = None                #6 bytes  sender hardware address
  __spa   = None                #4 bytes  sender protocol address
  __tha   = None                #6 bytes  target hardware address
  __tpa   = None                #4 bytes  target protocol address

  def __init__(self, op, dst, src, ip_dst, ip_src):
    self.op  = op
    self.dst = dst      # set tha
    self.src = src      # set sha

    self.tpa = ip_dst
    self.spa = ip_src
  #__init__

  def payload(self):
    return self.dst + self.src + self.ethertype + \
           self.htype + self.ptype + self.hlen + self.plen + self.op + \
           self.sha + self.spa + self.tha + self.tpa
  #payload

  def ethertype():
    doc = "The ethertype property."
    def fget(self):
      return self.__ethertype

    def fset(self, v):
      self.__ethertype = pack('!H', v)

    def fdel(self):
      del self.__ethertype

    return locals()
  #end definition ethertype property

  def src():
    doc = "The src property."
    def fget(self):
      return self.__src

    def fset(self, v):
      self.__src = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
      self.sha = self.src

    def fdel(self):
      del self.__src

    return locals()
  #end definition src property

  def dst():
    doc = "The dst property."
    def fget(self):
      return self.__dst

    def fset(self, v):
      self.__dst = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
      self.tha = self.dst

    def fdel(self):
      del self.__dst

    return locals()
  #end definition dst property

  def htype():
    doc = "The htype property."
    def fget(self):
      return self.__htype

    def fset(self, v):
      self.__htype = pack('!H', v)

    def fdel(self):
      del self.__htype

    return locals()
  #end definition htype property

  def ptype():
    doc = "The ptype property."
    def fget(self):
      return self.__ptype

    def fset(self, v):
      self.__ptype = pack('!H', v)

    def fdel(self):
      del self.__ptype

    return locals()
  #end definition ptype property

  def hlen():
    doc = "The hlen property."
    def fget(self):
      return self.__hlen

    def fset(self, v):
      self.__hlen = pack('!B', v)

    def fdel(self):
      del self.__hlen

    return locals()
  #end definition hlen property

  def plen():
    doc = "The plen property."
    def fget(self):
      return self.__plen

    def fset(self, v):
      self.__plen = pack('!B', v)

    def fdel(self):
      del self.__plen

    return locals()
  #end definition plen property

  def op():
    doc = "The op property."
    def fget(self):
      return self.__op

    def fset(self, v):
      self.__op = pack('!H', v)

    def fdel(self):
      del self.__op

    return locals()
  #end definition op property

  def sha():
    doc = "The sha property."
    def fget(self):
      return self.__sha

    def fset(self, v):
      self.__sha = v

    def fdel(self):
      del self.__sha

    return locals()
  #end definition sha property

  def spa():
    doc = "The spa property."
    def fget(self):
      return self.__spa

    def fset(self, v):
      self.__spa = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))

    def fdel(self):
      del self.__spa

    return locals()
  #end definition spa property

  def tha():
    doc = "The tha property."
    def fget(self):
      return self.__tha

    def fset(self, v):
      self.__tha = v

    def fdel(self):
      del self.__tha

    return locals()
  #end definition tha property

  def tpa():
    doc = "The tpa property."
    def fget(self):
      return self.__tpa

    def fset(self, v):
      self.__tpa = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))

    def fdel(self):
      del self.__tpa

    return locals()
  #end definition tpa property

  src   = property(**src())
  dst   = property(**dst())
  htype = property(**htype())
  ptype = property(**ptype())
  hlen  = property(**hlen())
  plen  = property(**plen())
  op    = property(**op())
  sha   = property(**sha())
  spa   = property(**spa())
  tha   = property(**tha())
  tpa   = property(**tpa())
  ethertype = property(**ethertype())
#class ARPSpoofPacket
